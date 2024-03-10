# testing.py
import sys

# Variable to store the previous message
previous_message = None

def process_message(message):
    global previous_message

    # Your logic for processing the message and generating a response
    # For now, just echoing the received message along with the previous message
    response = f"Hello, I have received your message '{message}'."

    if previous_message:
        response += f" Previous message was '{previous_message}'."

    # Update the previous_message variable
    previous_message = message

    return response

def main():
    while True:
        # Read the message from standard input
        message = sys.stdin.readline().strip()

        # Process the message and print the response to standard output
        response = process_message(message)
        print(response)
        # Ensure the output is flushed to be immediately available to the Node.js process
        sys.stdout.flush()

if __name__ == "__main__":
    main()
