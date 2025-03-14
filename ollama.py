"""Python script for handling messages via Ollama server.
Additionally translates English messages to Japanese,
And messages in other languages to English.
"""
# ollama.py
import logging
import os
import sys
from dotenv import load_dotenv
import requests
from googletrans import Translator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
# Instantiate translator
translator = Translator()
# Variable to store the previous message history
previous_messages = {}

def send_post_request(port_number, message, user):
    """This function appends the user's message to message history,
    then proceeds to send POST request to the LLM server, returning the response.

    Args:
        port_number (int): Port number of LLM server
        message (str): input message from user
        user (str): Twitch username of user

    Returns:
        str: Response message from LLM
    """

    if previous_messages.get(user):
        previous_messages[user].append(
            {
                "role":"user",
                "content":f"{message}"
            }
        )
    else:
        previous_messages[user] = [
            {
                "role":"user",
                "content":f"{message}"
            }
        ]

    message_history = previous_messages.get(user)

    url = f"http://localhost:{port_number}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model":os.getenv("OLLAMA_MODEL"),
        "messages":message_history,
        "stream":False
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=300)

        if response.status_code == 200:
            json_response = response.json()
            response_message = json_response.get("choices")[0]["message"]["content"]
            previous_messages[user].append(
                {
                    "role":"assistant",
                    "content":response
                }
            )
            return response_message
        else:
            logger.info("Error: %s", response.status_code)
            return f"{os.getenv('OLLAMA_MODEL')} is not available at the moment, please try again later."
    except requests.exceptions.RequestException as e:
        logger.info("Error from server: %s", e)
        return f"{os.getenv('OLLAMA_MODEL')} is not available at the moment, please try again later."

def process_message(username,message):
    """Translates English messages to Japanese,
    and messages in other languages to English

    Args:
        username (str): Twitch username of user
        message (str): message sent by user

    Returns:
        str: Translated message
    """
    
    # Detect language
    det_lang = translator.detect(message).lang # type: ignore
    if det_lang == 'en':
        tr_message = translator.translate(message, src='en', dest='ja').text # type: ignore
    else:
        tr_message = translator.translate(message, src='auto', dest='en').text # type: ignore
    # <class 'googletrans.models.Translated'>
    # Translated(src=en, dest=ja, text=テスト, pronunciation=Tesuto, extra_data="{'translat...")

    response = f"! {username}[{det_lang}]:" + tr_message

    return response

def main():
    """Main function of script.
    """
    while True:
        # Read the username and message from standard input
        username = sys.stdin.readline().strip()
        message = sys.stdin.readline().strip()

        # Process the message and print the response to standard output
        response = process_message(username, message)
        print(response)

        if message.startswith("!chat "):
            message = message[len("!chat "):]  # Remove "!chat " prefix
            port_number = os.getenv("LLM_PORT")

            content = send_post_request(port_number, message, username)
            print(f"###To {username}: {content}")
        # Ensure the output is flushed to be immediately available to the Node.js process
        sys.stdout.flush()

if __name__ == "__main__":
    main()
