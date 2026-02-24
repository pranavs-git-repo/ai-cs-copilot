customer_note = {
    "customer": "Acme Corp",
    "risk": "medium",
    "sentiment": "cautious",
    "next_actions": ["Follow up on firewall evaluation", "Schedule executive QBR"]
}
import json

json_output = json.dumps(customer_note, indent=2)
print(json_output)

parsed = json.loads(json_output)
print(parsed["risk"])  # Output: medium

customer_notes = [
    {"customer": "Acme Corp", "sentiment": "cautious"},
    {"customer": "Beta Inc", "sentiment": "happy"},
]

for note in customer_notes:
    print(f"{note['customer']} has sentiment {note['sentiment']}")


def summarize_risk(note):
    return f"{note['customer']} risk is {note['risk']}"

for note in customer_notes:
    note["risk"] = "medium"
    print(summarize_risk(note))


notes = [
    {"text": "Customer raised concerns about latency", "type": "issue"},
    {"text": "Executive sponsor missed QBR", "type": "engagement"},
]

issues = [n["text"] for n in notes if n["type"] == "issue"]
print(issues)
