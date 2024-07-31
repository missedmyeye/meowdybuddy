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
# Variable to store the previous message
previous_messages = {}

def send_post_request(port_number, message, user, twitch_bot_username):

    global previous_messages

    url = f"http://localhost:{port_number}/completion"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": f"<|start_header_id|>{user}<|end_header_id|>\n\n\
            {message}<|eot_id|>\n\
            <|start_header_id|>{twitch_bot_username}<|end_header_id|>\n",
        "stop": [f"{user}:",":"],
        "system_prompt":f"<|begin_of_text|><|start_header_id|>\n\n\
            You are {twitch_bot_username},a helpful and cheerful multilingual cat assistant who replies succinctly.\
            <|eot_id|>\n"
    }

    # Get the previous message for the user, if any
    # previous_message = str(previous_messages.get(user))

    # Update "prompt" in "system_prompt" if previous_message exists
    # if previous_message.startswith("!chat "):
    #     data["system_prompt"]["prompt"] += f" The previous message was {previous_message}"

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("content")
        else:
            print(f"Error: {response.status_code}")
            return None
    except:
        print("Error from server: ",Exception)

def process_message(username,message):
    global previous_messages

    # Get the previous message for the user, if any
    previous_message = previous_messages.get(username)

    # Your logic for processing the message and generating a response
    # For now, just echoing the received message along with the previous message
    # response = f"Hello, {username}, I have received your message '{message}'."

    # if previous_message:
    #     response += f" Your previous message was '{previous_message}'."
    # print(f"Hello, {username}, I have received your message '{message}'.")
    # print(f" Your previous message was '{previous_message}'.")

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
    previous_messages[username] = message

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
