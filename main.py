import streamlit as st
from ai.agent import chat
from ai.models.io import Chat
from ai.utils.ui import make_graph
from ai.utils.dot import dot

# Page setup
st.set_page_config(page_title="Research Agent", page_icon="📜", layout="wide")

# Title
st.title("📜 Agentic AI Researcher")

# Workflow (initial graph)
st.graphviz_chart(dot)

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
            answer: Chat = chat(query)

        # Show flow first
        st.subheader("🔄 Flow")
        dot_graph = make_graph(answer["flow"])
        st.graphviz_chart(dot_graph)

        # Then show answer
        st.subheader("📄 Answer")
        st.markdown(answer["response"])

    else:
        st.warning("⚠️ Please enter a query before analyzing.")
