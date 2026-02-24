from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
#print(f"API Key loaded: {os.getenv('OPENAI_API_KEY')[:10]}...")  # Print first 10 chars

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    return OpenAI(api_key=api_key)
