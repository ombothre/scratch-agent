import streamlit as st
from ai.agent import chat

# Page setup
st.set_page_config(page_title="Research Agent", page_icon="📜", layout="centered")

# Title
st.title("📜 Agentic AI Researcher")

# Input card
query = st.text_area(
    "💬 Enter your query:",
    placeholder="E.g. Legal document analysis on DPDPA",
    height=120
)

# Analyze button
if st.button("🔍 Analyze", use_container_width=True):
    if query.strip():
        with st.spinner("🤖 Analyzing..."):
            answer = chat(query)

        # Output card
        st.subheader("📄 Answer")
        st.markdown(answer)
    else:
        st.warning("⚠️ Please enter a query before analyzing.")
