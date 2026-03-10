# 🚀 Open Deep Search – AI-Powered Research Assistant

Open Deep Search is an **AI-powered research assistant** designed to help users summarize research topics, analyze research papers (PDFs), and ask context-aware follow-up questions.

The system uses a **multi-agent architecture** powered by modern AI frameworks such as **LangChain, LangGraph, Tavily Search API, and OpenRouter with Amazon Nova models**.

---

# 📌 Features

- 🔎 **Research Topic Summarization**  
  Generates structured academic summaries for research topics.

- 📄 **PDF Research Paper Summarization**  
  Users can upload research papers and receive concise summaries.

- 💬 **Context-Aware Follow-up Questions**  
  Allows users to ask questions based on previously generated summaries.

- 🤖 **Multi-Agent AI Architecture**  
  Uses planner, searcher, and writer agents coordinated with LangGraph.

- 🧠 **Session Memory**  
  Maintains chat history and research context across interactions.

- 🌐 **Streamlit Web Interface**  
  Provides an interactive chat-based interface similar to ChatGPT.

---

# 🏗 System Architecture

The system follows a layered architecture:

User → Streamlit Interface → Backend Router → LangGraph Multi-Agent System → LLM via OpenRouter → Response

### Main Components

**Streamlit UI**
- Chat interface
- PDF upload
- Session management

**Backend Router**
- Detects user intent
- Routes requests to appropriate processing pipelines

**LangGraph Multi-Agent System**

- Planner Agent – Determines task workflow  
- Searcher Agent – Retrieves research data using Tavily API  
- Writer Agent – Generates structured academic summaries  

**OpenRouter**
- Unified gateway for accessing large language models

**Amazon Nova Model**
- Generates research summaries and answers user questions.

---

# ⚙️ Technologies Used

- Python
- Streamlit
- LangChain
- LangGraph
- Tavily Search API
- OpenRouter API
- Amazon Nova Lite Model
- PyPDF
- python-dotenv

---

# 📂 Project Structure
Open-Deep-Search/ │ ├── interactive_assistant/ │   ├── app.py │   ├── backend.py │ ├── multiagent_system/ │   ├── graph.py │   └── agents/ │       ├── planner_agent.py │       ├── searcher_agent.py │       └── writer_agent.py │ ├── requirements.txt └── README.md
