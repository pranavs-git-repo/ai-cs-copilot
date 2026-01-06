import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

resp = client.responses.create(
    model="gpt-4.1-mini",
    input="In 3 bullet points, explain how AI can help Customer Success teams in cybersecurity."
)

print(resp.output_text)
