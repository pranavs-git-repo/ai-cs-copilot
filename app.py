import json
import streamlit as st

from cs_copilot import analyze_customer_context
#from rendering import json_to_markdown
from rendering import json_to_markdown, to_qbr_markdown, to_followup_email

# From-scratch RAG
from build_index import build_in_memory_index
from rag_pipeline import retrieve_context as retrieve_context_scratch

# LangChain RAG
from lc_retrieve import build_context_block as retrieve_context_lc

from customers import list_customer_ids
from rag_pipeline import retrieve_results  # new
from lc_retrieve import lc_results_as_dicts  # new
st.set_page_config(page_title="AI CS Copilot (RAG)", layout="wide")

st.title("AI Customer Success Copilot (RAG)")
st.caption("Synthetic data only • Retrieval-grounded • Structured JSON output with citations")

PRESET_QUESTIONS = {
    "Renewal risk + next actions": "What are the top renewal risks and churn indicators for this account? Provide next actions.",
    "Executive QBR summary": "Create an executive-ready QBR summary: key wins, challenges, and recommendations.",
    "Support pain points": "What are the recurring support issues and likely root causes? Recommend remediation steps."
}

with st.sidebar:
    st.header("Controls")
    # NEW: Customer selection
    customer_ids = list_customer_ids()
    customer_id = st.selectbox("Customer", customer_ids)
    rag_backend = st.radio("RAG backend", ["From-scratch", "LangChain"], index=0)
    top_k = st.slider("Top-K retrieved chunks", min_value=3, max_value=10, value=6, step=1)
    preset = st.selectbox("Preset question", list(PRESET_QUESTIONS.keys()))
    use_preset = st.checkbox("Use preset", value=True)
    export_format = st.selectbox("Export format", ["Generic", "QBR", "Follow-up Email"])

question = PRESET_QUESTIONS[preset] if use_preset else st.text_area("Enter your question", height=120)

run = st.button("Run Copilot")

if run:
    # 1) Retrieve context
    with st.spinner("Retrieving relevant context..."):
        if rag_backend == "From-scratch":
            index = build_in_memory_index()
            context = retrieve_context_scratch(
                query=question,
                index=index,
                top_k=top_k,
                customer_id=customer_id,   # NEW
            )
            hits = retrieve_results(
                query=question,
                index=index,
                top_k=top_k,
                customer_id=customer_id
            )
        else:
            context = retrieve_context_lc(
                query=question,
                top_k=top_k,
                customer_id=customer_id,   # NEW
            )
            hits = lc_results_as_dicts(
                query=question,
                top_k=top_k,
                customer_id=customer_id
            )

    # 2) Generate structured output
    with st.spinner("Generating CS insights..."):
        result = analyze_customer_context(context=context, question=question)
#        md = json_to_markdown(result, title=f"{customer_id} — {preset}")
        if export_format == "QBR":
            md = to_qbr_markdown(result, customer_id=customer_id)
        elif export_format == "Follow-up Email":
            md = to_followup_email(result, customer_id=customer_id)
        else:
            md = json_to_markdown(result, title=f"{customer_id} — {preset}")

    # 3) Display
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Structured Output (JSON)")
        st.json(result)
        st.subheader("Export (Markdown)")
        st.code(md, language="markdown")
        safe_name = export_format.replace(" ", "_").lower()
        st.download_button(
            label="Download Markdown",
            data=md,
            file_name=f"{customer_id}_{safe_name}.md",
            mime="text/markdown",
        )

        st.subheader("Raw JSON")
        st.code(json.dumps(result, indent=2), language="json")

    with col2:
        st.subheader("Retrieved Context (with citations)")
        st.text_area("Context", value=context, height=650)
        st.subheader("Evidence (Top retrieved chunks)")

        for i, h in enumerate(hits, start=1):
            if rag_backend == "From-scratch":
                title = f"{i}. score={h['score']} — {h['chunk_id']} ({h['source_file']})"
                body = h["text"]
            else:
                title = f"{i}. score={h['score']} — {h['citation']}"
                body = h["text"]

            with st.expander(title):
                st.write(body)

