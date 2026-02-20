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
