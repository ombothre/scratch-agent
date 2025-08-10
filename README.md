# 📜 Agentic AI Researcher

This project is an **AI-powered research agent** built from scratch using pure Python, without any frameworks like LangChain or LangGraph. It leverages a custom-built graph-based workflow to orchestrate multiple Large Language Models (LLMs) and external tools to perform in-depth research and generate a comprehensive, structured research paper. It could be used to answer other queries too using its tool for real time information access.

## 🤖 Agent Workflow
<img width="405" height="553" alt="image" src="https://github.com/user-attachments/assets/c349860b-4f3b-4fe6-b7d8-c04a2146b2dd" />


The user interface is powered by **Streamlit**, providing a simple and intuitive way to interact with the agent.

## ✨ Features

  - **Custom Agentic Workflow**: A state machine (graph) orchestrates the research process, moving from initial query to final output.
  - **Pure Python Implementation**: No dependencies on complex AI frameworks, offering full control and a deep understanding of the underlying logic.
  - **Dual-LLM Architecture**: Utilizes two different LLMs for specialized tasks: one for initial research and tool selection, and another for synthesizing a final, polished research paper.
  - **Integrated Tool Use**: Capable of using external tools for real-time web searches and finding academic research papers.
  - **Structured Output**: Generates a professional, detailed research paper in Markdown format, complete with a title, abstract, introduction, and references.
  - **Streamlit UI**: A clean, easy-to-use web interface for submitting queries and viewing results.

## 🧠 How It Works

The agent's logic is defined by a directed graph (state machine) that processes a user's query through a series of nodes:

1.  **`start_node`**: Initializes the state with the user's query.
2.  **`research_llm`**: An LLM (referred to as "researcher") analyzes the query. It determines if external tools are needed and, if so, formulates specific queries for them.
3.  **`tool_condition`**: This node checks if the researcher LLM requested tools.
      - If **yes**, it executes the tools (`web_search` and/or `research_papers`) and updates the state with the results. The workflow then moves to the `output_llm`.
      - If **no**, it skips tool execution and moves directly to the `end_node`, as the researcher LLM was able to answer directly.
4.  **`output_llm`**: A second, specialized LLM (referred to as "outputer") takes all the information gathered—the researcher's initial thoughts and any tool results—and synthesizes it into a complete, well-structured research paper in Markdown format.
5.  **`end_node`**: The final node, which halts the workflow and returns the generated content.

## 🛠️ Prerequisites

To run this project, you need:

  - A Python environment (version 3.10+)
  - API keys for the services used:
      - Google Gemini API (for LLM access)
      - Tavily Search API (for `web_search`)

Once you have your keys, add them to a `.env` file in the root directory:

```bash
# .env file
LLM_API_KEY="your_gemini_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
```

## 🚀 Installation and Usage

1.  **Sync Dependencies**: This project uses `uv` for dependency management.

    ```bash
    uv sync
    ```

2.  **Run the App**: Start the Streamlit server to launch the web interface.

    ```bash
    streamlit run main.py
    ```

3.  **Use the Agent**: Open your web browser and navigate to the local URL provided by Streamlit (e.g., `http://localhost:8501`). Enter a research-related query in the text box and click "Analyze" to see the agent in action.
