# test_retrieval.py

from build_index import build_in_memory_index
from retrieval import retrieve_top_k

def main():
    index = build_in_memory_index()

    query = "Summarize renewal risks and vendor competition signals."
    results = retrieve_top_k(query=query, index=index, top_k=5)

    print("\n=== TOP RETRIEVAL RESULTS ===\n")
    for r in results:
        print(f"- score={r['score']} | {r['chunk_id']} ({r['source_file']})")
        print(f"  {r['text'][:220].replace('\\n', ' ')}")
        print()

if __name__ == "__main__":
    main()
