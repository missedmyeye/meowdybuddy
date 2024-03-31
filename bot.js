require('dotenv').config();
const fs = require('fs');
const fetch = require("node-fetch")
const tmi = require('tmi.js');
const { spawn } = require('child_process');

var config = null

function instantiateConfigs() {
    // Read the content of the JSON file
    const configFile = fs.readFileSync('tokens.json', 'utf8');
  
    // Parse the JSON content
    config = JSON.parse(configFile);
  
    // Instantiate configuration options
    const client = new tmi.Client({
      connection: {
        reconnect: true
      },
      channels: [
        process.env.TWITCH_CHANNEL
      ],
      identity: {
        username: process.env.TWITCH_BOT_USERNAME,
        password: config.access_token
      },
    });
  
    return client;
}

// Call the function to instantiate the configurations
var twitchClient = instantiateConfigs();

// Initialize an empty map to track users who have chatted
const usersChatted = new Map();
const excludedBots = process.env.BOT_LIST.split(',').map(bot => bot.toLowerCase());

// Access the list of keywords from the environment variables
const botMessages = JSON.parse(fs.readFileSync('bot_messages.json', 'utf8'));

function pythonSpawn(){
    // Spawn the Python process
    const pythonProcess = spawn('python', [process.env.PYTHON_SCRIPT]);

    // Event handler for receiving data from the Python process
    pythonProcess.stdout.on('data', (data) => {
        const response = data.toString().trim();
        console.log('Received response from Python process:\n', response);

        // Perform actions or send the response to the chat
        twitchClient.say(process.env.TWITCH_CHANNEL, response);
    });

    // Event handler for handling errors in the Python process
    pythonProcess.stderr.on('data', (data) => {
        console.error('Error from Python process:', data.toString().trim());
    });

    // Event handler for when the Python process exits
    pythonProcess.on('exit', (code, signal) => {
        console.log(`Python process exited with code ${code} and signal ${signal}`);
    });

    return pythonProcess;
};

// Function to refresh the access token
async function refreshAccessToken(refreshToken) {
    try {
        console.log(`refresh token: ${refreshToken}`)
        const clientId = process.env.TWITCH_CLIENT_ID
        const clientSecret = process.env.TWITCH_CLIENT_SECRET
        const response = await fetch(
            "https://id.twitch.tv/oauth2/token",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
              },
              body: `grant_type=refresh_token&refresh_token=${refreshToken}&client_id=${clientId}&client_secret=${clientSecret}`,
            }
        );
        const data = await response.json();
        console.log(data);

        // Save the new tokens to tokens.json
        tokens ={};
        if (data.access_token != null && data.refresh_token != null) {
            tokens = {
                access_token: data.access_token,
                refresh_token: data.refresh_token,
                scope: data.scope,
                token_type: data.token_type,
                expires_in: data.expires_in
            };

            fs.writeFileSync('tokens.json', JSON.stringify(tokens, null, 2));
        }
        
        return tokens;
    } catch (error) {
        console.error('Error refreshing access token:', error.message);
        throw error; // Rethrow the error for the caller to handle
    }
}


// Function to connect the client
var connectFail = 0

async function connectClient() {
    try {
        await twitchClient.connect();
        console.log('Connected to Twitch chat!');
    } catch (error) {
        connectFail += 1;
        // Terminate if failed to connect > 3 times
        if (connectFail > 3){
            console.error(`Multiple failed connection attempts. Error: ${error}\nAborting...`);
            return error;
        }

        if (error === 'Login authentication failed') {
            console.error(error);
            // If unauthorized, try refreshing the access token
            console.log('Refreshing access token...');
            tokens = await refreshAccessToken(
                config.refresh_token
            );
            // Reread config file and parse again
            twitchClient = instantiateConfigs();
            // Retry connecting with the updated access token
            await connectClient();
        } else {
            console.error('Error connecting to Twitch chat:', error);
        }
    }
}
async function main() {
    // Start connecting the client
    await connectClient();
    // Start up Python process
    const pythonProcess = pythonSpawn();

    twitchClient.on('message', async (channel, context, message) => {
        console.log('channel', {
            channel,
            user: context.username,
            message
        });

        const isNotBot = !excludedBots.includes(context.username.toLowerCase());

        // Check if the user has chatted during the current stream
        const chatCount = usersChatted.get(context.username);

        if ( isNotBot) {
            console.log(`${context.username} messages in stream: ${chatCount}`)
            
            // Respond to first message in stream, trigger Nightbot !hi command
            if ( !chatCount ) {
                twitchClient.say(channel, `Ohowdy gozaimasu! Welcome to the stream @${context.username} ~ GlitchCat GlitchCat GlitchCat `);
                // Mark the user as having chatted
                usersChatted.set(context.username, 1);
                console.log(usersChatted)
            }
            // If user sends more than 1 message, shoutout to user
            else if ( chatCount == 1 ){  
                twitchClient.say(channel, `Go check out @${context.username} at Twitch.tv/${context.username} Poooound`);
                usersChatted.set(context.username, chatCount+1);
            };

            // Send the username and message to the Python process for processing
            // Ensure message is not chat command
            if (!message.startsWith("!") || !/^![a-zA-Z]/.test(message)) {
                pythonProcess.stdin.write(`${context.username}\n${message}\n`);
            }
            else if (message.startsWith("!chat ")){
                console.log(`LLM Input (WIP): ${message}`)
            }

        } else {
            // Auto-check and respond to bots
            for (const key of Object.keys(botMessages)) {
                if (message.includes(key)) {
                    const response = botMessages[key];
                    // Respond with the corresponding value
                    twitchClient.say(channel, response);
                    break; // Stop checking once a match is found
                }
            }
        }

        
    });
}

main()