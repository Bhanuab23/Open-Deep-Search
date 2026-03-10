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

---

# 📂 Project Structure

```
Open-Deep-Search/
│
├── interactive_assistant/
│   ├── app.py              
│   └── backend.py          
│
├── multiagent_system/
│   ├── graph.py           
│   └── agents/
│       ├── planner_agent.py   
│       ├── searcher_agent.py 
│       └── writer_agent.py    
│
├── requirements.txt        
├── .env                     
└── README.md                
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Open-Deep-Search.git
cd Open-Deep-Search
```

---

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root directory and add your API keys:

```
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

These keys are required for the LLM and research retrieval functionality.

---

## ▶️ Running the Application

Start the Streamlit application with the following command:

```bash
python -m streamlit run interactive_assistant/app.py
```

After running, open your browser and navigate to:

```
http://localhost:8501
```

---

## 🔍 Example Workflow

1. Enter a research topic such as:

```
Natural Language Processing
```

2. The system generates a structured academic summary.

3. Upload a research paper PDF to receive a summarized version.

4. Ask follow-up questions such as:

```
What are the main challenges mentioned in this research?
```

The system answers using only the previously generated research context.

---

## ⚠️ Challenges Faced

- Controlling hallucinations in LLM outputs  
- Maintaining research context for follow-up questions  
- Designing multi-agent workflows using LangGraph  
- Managing API keys and environment configuration  
- Implementing multi-chat session memory in Streamlit

---

## 🚀 Future Improvements

- Multi-paper comparison
- Citation extraction
- Semantic search for research papers
- Cloud deployment
- Research trend visualization

---

## 📜 License

This project is developed for **educational and research purposes**.