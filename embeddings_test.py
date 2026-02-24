from openai import OpenAI
from ai_client import get_client

client = get_client()

def embed_text(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [e.embedding for e in response.data]
