from dotenv import load_dotenv
from google import genai
import os
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

load_dotenv()

def main():
    # load the API key from the environment variable
    API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")
    print(API_KEY_GEMINI)

    client = genai.Client(api_key=API_KEY_GEMINI)

    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=["explain how Sparse Autoencoder works"],
    )

    for chunk in response:
        print(chunk.text)

if __name__ == "__main__":
    main()
