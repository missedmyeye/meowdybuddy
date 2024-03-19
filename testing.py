# testing.py
import sys
from googletrans import Translator

# Instantiate translator
translator = Translator()
# Variable to store the previous message
previous_messages = {}

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

    response = translator.translate(message, src='en', dest='ja').text
    # <class 'googletrans.models.Translated'>
    # Translated(src=en, dest=ja, text=テスト, pronunciation=Tesuto, extra_data="{'translat...")
    if translator.detect(response).lang == 'ja':
        response = (f"! {username}:" + response)
    else:
        response = ''

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
        # Ensure the output is flushed to be immediately available to the Node.js process
        sys.stdout.flush()

if __name__ == "__main__":
    main()
