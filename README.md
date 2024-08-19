# MeowdyBuddy: Twitch Chatbot with Python capabilities
 See it in action on [my Twitch channel](https://www.twitch.tv/youmissedmyeye)!
## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Package Installation/Environment Setup](#package-installationenvironment-setup)
- [Creating a Twitch Chatbot](#creating-a-twitch-chatbot)
- [Set Up .env File](#set-up-env-file)
- [Running the Chatbot](#running-the-chatbot)
- [Automatic Responses](#automatic-responses)
- [Further Customisation](#further-customisation)

## Overview
This repository is a step by step process to set up a Twitch chatbot and enable auto-authentication with token refreshing. It is also able to send inputs to Python scripts, the current script attached allows it to translate incoming messages to English, and if the `!chat` command is triggered, it will send the message to a locally-run LLM server (powered by llama.cpp in my use case) for a response.
## Prerequisites
This repository is run and tested on MacBook Air with Apple M2 Chip (ARM64/Aarch64 architecture).<br>
MacOS Sonoma 14.2.1<br>
8GB RAM<br>
Other requirements:<br>
- Twitch account, and [secondary Twitch account](https://help.twitch.tv/s/article/creating-an-account-with-twitch?language=en_US#AdditionalAccounts) for your chatbot
- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
- [Homebrew (For MacOS/Linux)](https://brew.sh/)
- Node.js (v18.19.0)
    ```bash
    brew install node@18
    ```
    Run `node -v` to check on your version, it should return `v18.19.1`. If you get a response `node: command not found`, run the command provided when you install node@18:<br>
    ```
    If you need to have node@18 first in your PATH, run:
    echo 'export PATH="/opt/homebrew/opt/node@18/bin:$PATH"' >> ~/.zshrc
    ```
- [Twitch CLI](https://dev.twitch.tv/docs/cli/) (Currently using version 1.1.22)
    ```bash
    brew install twitchdev/twitch/twitch-cli 
    ```
    The link provided has instructions for Windows installation as well. To check version, run `twitch version`.
## Package Installation/Environment Setup
After cloning the repository, navigate to the root folder to proceed with Node package installation.<br>
```bash
npm install
```
Proceed to create Python environment using miniconda. Adjust `requirements.txt` as per your needs if you are using a different Python script.
```
conda env create -n env_name python=3.10
conda activate env_name
pip install -r requirements.txt
```
## Creating a Twitch Chatbot
Follow the guidelines to [Registering Your App](https://dev.twitch.tv/docs/authentication/register-app/). 
- Assign any name you wish, your chatbot's name will be the secondary account you created. 
- For `OAuth Redirect URLs`, assign it to `http://localhost:3000`. 
- `Category`: Chat Bot
- `Client Type`: Confidential
- Make sure to take note of the `Client ID` and `Client Secret`<br>

Proceed with [configuring your Twitch CLI](https://dev.twitch.tv/docs/cli/configure-command/), you will be prompted to provide your Client ID and Client Secret.<br>
Once that is done, log in to your browser with your secondary account, i.e. *your chatbot's account*.

Next on the agenda is to [Get a User Access Token](https://dev.twitch.tv/docs/cli/token-command/#user-access-token).
Specifying the scope here is crucial, as it determines your app's access to information. Here is a [list of scopes](https://dev.twitch.tv/docs/authentication/scopes/#twitch-api-scopes) that you may wish to use. For a chatbot, the scopes required are `chat:read` and `chat:edit`, meaning to read and write to the channel. So the command will be:
```bash
twitch token -u -s 'chat:read chat:edit'
```
A browser will be opened for you to authorize with your chatbot account, following which your `User Access Token` and `Refresh Token` will be provided in your terminal output. Do not share this information. Please save the provided information in the repository root folder under `tokens.json` in the following format:
```
{
  "access_token": "xxxxxxxxxxxxxxxxxxx",
  "refresh_token": "xxxxxxxxxxxxxxxxxxx",
  "scope": [
    "chat:edit",
    "chat:read"
  ],
  "token_type": "bearer",
  "expires_in": 14688
}
```
## Set Up .env File
Create a file in your repository root folder `.env`. It should have the following parameters in this format:
```
TWITCH_CHANNEL = "myTwitchChannel"
TWITCH_BOT_USERNAME = "ChatBotName"
BOT_LIST=bot1,bot2,bot3,ChatBotName
TWITCH_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxx"
TWITCH_CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxx"
PYTHON_SCRIPT = "ollama.py"
OLLAMA_MODEL = "llama3.1"
LLM_PORT = 11434
```
- `TWITCH_CHANNEL`: The name of your Twitch channel.
- `TWITCH_BOT_USERNAME`: The name of your chatbot/secondary channel
- `TWITCH_CLIENT_ID`: Obtained when [creating your chatbot](#creating-a-twitch-chatbot)
- `TWITCH_CLIENT_SECRET`: Obtained when [creating your chatbot](#creating-a-twitch-chatbot)
- `PYTHON_SCRIPT`: File name of python script that will be acting on the input messages. Messages from a user in `BOT_LIST` or a chat command e.g. "!hi user1234" will be ignored.
- `BOT_LIST`: List of excluded bots/users. Python script will not act on messages from them, make sure to include `TWITCH_BOT_USERNAME`. I simultaneously run a chatbot [Nightbot](https://nightbot.tv/)(which I used before this project) and the extension [Pokemon Community Game](https://www.twitch.tv/directory/category/pokemon-community-game), so I don't want my Python script to be acting on their automated messages as well.
- `OLLAMA_MODEL`: If using `ollama.py` to interact with an LLM running on Ollama, use this parameter to specify the model name. Include the tag if necessary, e.g. `llama3.1:8b`
- `LLM_PORT`: localhost port which your LLM server has exposed. Default port for llama.cpp is `8080`, while Ollama's default is `11434`.
## Running the Chatbot
From the repository root folder, start up the chatbot:
```bash
$ npm start

> meowdybuddy@1.0.0 start
> node bot.js

Connected to Twitch chat!
```
Your access token expires every few hours, so in the event it has expired when you start it up, it should refresh your access token and update in `tokens.json` automatically. Then it will attempt to connect to Twitch again.
```bash
$ npm start

> meowdybuddy@1.0.0 start
> node bot.js

[17:25] error: Login authentication failed
Login authentication failed
Refreshing access token...
refresh token: abcdefgh
{
  access_token: 'xxxxxxxxxxxxxxx',
  expires_in: 14404,
  refresh_token: 'abcdefgh',
  scope: [ 'chat:edit', 'chat:read' ],
  token_type: 'bearer'
}
Connected to Twitch chat!
```
Make sure your local LLM server is up and running, and you should be good to go. Input "!chat " before your message to talk to your LLM! Have fun!
## Automatic Responses
The file `bot_messages.json` contains a dictionary of messages that the chatbot will auto respond to, if mentioned by the channel owner or any of the users in `BOT_LIST`. The key is the message it will look out for, while the value is the automatic response.
```
{
    "Bot message goes here.":"Your intended response goes here."
}
```
For example, if the channel owner sends the message "Bot message goes here.", the chatbot will automatically reply "Your intended response goes here."
## Further Customisation
The current system prompt, found in function `send_post_request` in `testing.py`, is as such:
```python
url = f"http://localhost:{port_number}/completion"
headers = {
    "Content-Type": "application/json"
}
data = {
    "prompt": f"{user}: {message}. {twitch_bot_username}:",
    "stop": [f"{user}:",":"],
    "system_prompt": {
        "prompt": f"You are {twitch_bot_username}, a cheerful and helpful cat assistant \
            who speaks like a cat. You occasionally pepper your conversation with cat sounds.",
        "anti_prompt": f"{user}:",
        "assistant_name": f"{twitch_bot_username}:"
    }
}
```
I currently use llama2-7b-chat, quantized to 4 bits. Do adjust the prompt accordingly to cater to your specific needs. If you are running your model on the cloud, do update the URL as well. This will be made configurable in future updates.
