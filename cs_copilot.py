import json
from ai_client import get_client
from prompts import (
    CS_COPILOT_SYSTEM_PROMPT,
    CS_COPILOT_JSON_INSTRUCTIONS,
    CS_COPILOT_CITATION_RULES,
)

def analyze_customer_context(context: str, question: str) -> dict:
    """
    Analyze retrieved customer context and return structured CS insights as JSON.
    """
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": CS_COPILOT_SYSTEM_PROMPT},
            {"role": "user", "content": f"""
{CS_COPILOT_JSON_INSTRUCTIONS}
{CS_COPILOT_CITATION_RULES}

Task:
Using ONLY the provided context, answer the question and produce the JSON schema.

Question:
{question}

Context:
{context}
"""}
        ],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned by model:\n{raw_output}")
