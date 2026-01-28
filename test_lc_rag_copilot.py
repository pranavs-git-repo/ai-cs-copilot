# test_lc_rag_copilot.py

import json
from lc_retrieve import build_context_block, retrieve_top_k
from cs_copilot import analyze_customer_context

def main():
    question = "What are the top renewal risks and churn indicators for this account? Provide next actions."
    context = build_context_block(question, top_k=6)

    result = analyze_customer_context(context=context, question=question)

    print("\n=== LANGCHAIN RETRIEVAL (top hits) ===\n")
    hits = retrieve_top_k(question, top_k=6)
    for citation, text, score in hits:
        print(f"- {citation} score={score:.4f}")
        print(f"  {text[:220].replace('\\n', ' ')}\n")

    print("\n=== CONTEXT (preview) ===\n")
    print(context[:1200])

    print("\n=== RAG CS COPILOT STRUCTURED OUTPUT ===\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
