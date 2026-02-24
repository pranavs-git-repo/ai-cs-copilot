from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
#print(f"API Key loaded: {os.getenv('OPENAI_API_KEY')[:10]}...")  # Print first 10 chars

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say hello"}]
)

# Print the entire first choice
print(response.choices[0].message.content)

# Output (formatted):
# Choice(
#     finish_reason='stop',
#     index=0,
#     message=ChatCompletionMessage(
#         content='Hello! How can I help you?',
#         role='assistant'
#     )
# )