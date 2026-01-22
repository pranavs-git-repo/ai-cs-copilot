import json
from build_index import build_in_memory_index
from rag_pipeline import retrieve_context
from cs_copilot import analyze_customer_context

def main():
    index = build_in_memory_index()

    question = "What are the top renewal risks and churn indicators for this account? Provide next actions."
    context = retrieve_context(query=question, index=index, top_k=6)

    result = analyze_customer_context(context=context, question=question)

    print("\n=== RETRIEVED CONTEXT (preview) ===\n")
    print(context[:1200])  # preview first ~1200 chars

    print("\n=== RAG CS COPILOT STRUCTURED OUTPUT ===\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
