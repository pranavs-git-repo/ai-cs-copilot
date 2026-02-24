# rendering.py

from __future__ import annotations
from typing import Dict, List, Any

def _bullets(items):
    if not items:
        return "- (none)"

    # If the model accidentally returns a string instead of list
    if isinstance(items, str):
        items = [items]

    return "\n".join([f"- {x}" for x in items])


def json_to_markdown(result: Dict[str, Any], title: str = "CS Copilot Output") -> str:
    sentiment = result.get("sentiment", "Unknown")

    md = []
    md.append(f"# {title}")
    md.append("")
    md.append(f"**Sentiment:** {sentiment}")
    md.append("")

    md.append("## Risk Signals")
    md.append(_bullets(result.get("risk_signals", [])))
    md.append("")

    md.append("## Churn Indicators")
    md.append(_bullets(result.get("churn_indicators", [])))
    md.append("")

    md.append("## Recommended Actions")
    md.append(_bullets(result.get("recommended_actions", [])))
    md.append("")

    md.append("## Executive Summary")
    md.append(_bullets(result.get("executive_summary", [])))
    md.append("")

    return "\n".join(md)

def to_qbr_markdown(result: Dict[str, Any], customer_id: str) -> str:
    md = []
    md.append(f"# QBR Executive Summary — {customer_id}")
    md.append("")
    md.append(f"**Sentiment:** {result.get('sentiment', 'Unknown')}")
    md.append("")

    md.append("## Key Wins / Progress")
    md.append(_bullets(result.get("executive_summary", [])))
    md.append("")

    md.append("## Risks & Challenges")
    md.append(_bullets(result.get("risk_signals", [])))
    md.append("")

    md.append("## Churn Indicators")
    md.append(_bullets(result.get("churn_indicators", [])))
    md.append("")

    md.append("## Recommended Actions (Next 30 Days)")
    md.append(_bullets(result.get("recommended_actions", [])))
    md.append("")

    return "\n".join(md)


def to_followup_email(result: Dict[str, Any], customer_id: str) -> str:
    # Keep this short and copy/paste friendly
    subject = f"Follow-up and next steps — {customer_id}"

    body = []
    body.append(f"Subject: {subject}")
    body.append("")
    body.append("Hi team,")
    body.append("")
    body.append("Thank you for the discussion. Here’s a quick recap and the proposed next steps:")
    body.append("")
    body.append("Key points:")
    body.append(_bullets(result.get("executive_summary", [])))
    body.append("")
    body.append("Next steps:")
    body.append(_bullets(result.get("recommended_actions", [])))
    body.append("")
    body.append("Please let me know if you’d like to adjust priorities or add anything.")
    body.append("")
    body.append("Best,")
    body.append("[Your Name]")
    return "\n".join(body)