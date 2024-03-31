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

    # Detect language
    det_lang = translator.detect(message).lang
    if det_lang == 'en':
        tr_message = translator.translate(message, src='en', dest='ja').text
    else:
        tr_message = translator.translate(message, src='auto', dest='en').text
    # <class 'googletrans.models.Translated'>
    # Translated(src=en, dest=ja, text=テスト, pronunciation=Tesuto, extra_data="{'translat...")
    
    response = (f"! {username}[{det_lang}]:" + tr_message)

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
