import os
import logging

import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

def generate_text_with_gemini(
    api_key=google_api_key,
    model_name="gemini-2.0-flash",
    system_instruction="You are a helpful assistant",
    prompt=[
        {
            "role":"user",
            "parts":["Hello."]
            }
        ]
):
    """
    Generates text using the Google Gemini API with a specified system instruction.

    Args:
        api_key (str): Your Google API key.
        model_name (str): The name of the Gemini model to use (e.g., "gemini-2.0-flash").
        system_instruction (str): The system instruction to set the context.
        prompt (str): The user prompt.

    Returns:
        str: The generated text response, or None if an error occurs.
    """

    # logger.info("Generating text with Gemini...")
    # logger.info("Input:\n%s", prompt)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction
        )

    try:
        response = model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(
            ),
            safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
             },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
             }
            ],
        )
        # logger.info(response)
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Load the API key from the .env file
    api_key_eg = os.getenv("GOOGLE_API_KEY")

    if not api_key_eg:
        print(
            "Error: GOOGLE_API_KEY not found. "
            "Please set it in your environment or .env file."
        )
        exit()

    model_name_eg = "gemini-2.0-flash"  # Or any specific model you'd like
    system_instruction_eg = """
        You are Meowdy Buddy, a helpful and cheerful multilingual cat assistant
        who replies succinctly, occasionally adding cat sounds to speech.
        """
    prompt_eg = [
        {
            "role":"user",
            "parts":["Hey there! Tell me a nice and interesting story."]
            }
        ]

    response_text = generate_text_with_gemini(
        api_key_eg, model_name_eg, system_instruction_eg, prompt_eg
    )

    if response_text:
        print("Generated Text:")
        print(response_text)