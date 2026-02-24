from ai_client import get_client
from cs_copilot import analyze_customer_notes
from sample_data import SAMPLE_CUSTOMER_NOTES
import json

def main():
    result = analyze_customer_notes(SAMPLE_CUSTOMER_NOTES)
    print("\n=== CS COPILOT STRUCTURED OUTPUT ===\n")
    print(json.dumps(result, indent=2))
    print(result)

if __name__ == "__main__":
    main()
