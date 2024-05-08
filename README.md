 MeowdyBuddy: Twitch Chatbot with Python capabilities
## Table of Contents
- Overview
- Pre-requisites
- Package Installation/Environment Setup
- Creating a Twitch Chatbot

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
A browser will be opened for you to authorize with your chatbot account, following which your `User Access Token` and `Refresh Token` will be provided in your terminal output.