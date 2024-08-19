# llama3-8b-cpt-sea-lionv2-instruct.py
import os
import sys
from dotenv import load_dotenv
import requests
from googletrans import Translator

# Load environment variables from .env file
load_dotenv()
# Instantiate translator
translator = Translator()
# Variable to store the previous message history
previous_messages = {}

def send_post_request(port_number, message, user, twitch_bot_username):

    global previous_messages

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

    url = f"http://localhost:{port_number}/api/chat"
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
            response = json_response.get("message")["content"]
            previous_messages[user].append(
                {
                    "role":"assistant",
                    "content":response
                }
            )
            return json_response.get("message")["content"]
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception:
        print("Error from server: ",Exception)

def process_message(username,message):
    # Detect language
    det_lang = translator.detect(message).lang
    if det_lang == 'en':
        tr_message = translator.translate(message, src='en', dest='ja').text
    else:
        tr_message = translator.translate(message, src='auto', dest='en').text
    # <class 'googletrans.models.Translated'>
    # Translated(src=en, dest=ja, text=テスト, pronunciation=Tesuto, extra_data="{'translat...")

    response = f"! {username}[{det_lang}]:" + tr_message

    # Update the previous message for the user
    # previous_messages[username] = message

    return response

def main():
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
            twitch_bot_username = os.getenv("TWITCH_BOT_USERNAME")

            content = send_post_request(port_number, message, username, twitch_bot_username)
            print(f"###To {username}: {content}")
        # Ensure the output is flushed to be immediately available to the Node.js process
        sys.stdout.flush()

if __name__ == "__main__":
    main()
