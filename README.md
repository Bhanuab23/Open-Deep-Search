Open Deep Search – AI-Powered Research Assistant
An AI-powered research assistant that helps users summarize research topics, analyze research papers (PDFs), and ask context-aware follow-up questions using a multi-agent architecture powered by LLMs.
The system integrates Streamlit, LangChain, LangGraph, Tavily Search API, and OpenRouter (Amazon Nova model) to provide structured academic summaries and intelligent research exploration.
Features
Research Topic Summarization
Users can enter a research topic, and the system generates a structured academic summary synthesized from research sources.
PDF Research Paper Summarization
Users can upload research papers in PDF format and receive a concise, structured summary including key insights.
Context-Aware Follow-up Questions
After generating a summary, users can ask follow-up questions. The system answers strictly based on the previously generated research context.
Multi-Agent AI Architecture
The system uses a planner agent, searcher agent, and writer agent orchestrated using LangGraph to simulate a research workflow.
Chat-Based Interface
A Streamlit-based chat interface supports multiple conversations and session memory, similar to ChatGPT.
System Architecture
The system follows a layered architecture:
User → Streamlit Interface → Backend Router → LangGraph Multi-Agent System → LLM via OpenRouter → Response
Components include:
Streamlit UI
Handles user interaction, PDF upload, and chat sessions.
Session Memory
Stores chat history, research context, and source type for follow-up questions.
Backend Router
Analyzes user input and routes it to appropriate pipelines such as topic summarization, PDF summarization, or question answering.
LangGraph Multi-Agent System
Planner Agent – Determines task workflow
Searcher Agent – Retrieves research information using Tavily API
Writer Agent – Generates structured academic summaries
OpenRouter Provides a unified interface to large language models.
Amazon Nova Model Generates research summaries and answers questions.
Methodology
The user provides a research topic or uploads a PDF.
The system detects the intent of the input.
The planner agent determines the processing strategy.
The searcher agent retrieves research information using Tavily.
The writer agent synthesizes the information into a structured academic summary.
The summary is stored as research context.
Follow-up questions are answered strictly using this stored context.
Technologies Used
Python
Streamlit – Web interface
LangChain – LLM workflow management
LangGraph – Multi-agent orchestration
Tavily API – Research search
OpenRouter – LLM gateway
Amazon Nova Lite – Language model
PyPDF – PDF text extraction
Python-dotenv – Environment variable management
Project Structure
Copy code

Open-Deep-Search/
│
├── interactive_assistant/
│   ├── app.py
│   ├── backend.py
│
├── multiagent_system/
│   ├── graph.py
│   ├── run.py
│   └── agents/
│       ├── planner_agent.py
│       ├── searcher_agent.py
│       └── writer_agent.py
│
├── mini_research_agent/
│
├── requirements.txt
└── README.md
Installation
1. Clone the repository
Copy code

git clone https://github.com/yourusername/Open-Deep-Search.git
cd Open-Deep-Search
2. Create a virtual environment
Copy code

python -m venv venv
Activate environment
Windows:
Copy code

venv\Scripts\activate
Linux / Mac:
Copy code

source venv/bin/activate
3. Install dependencies
Copy code

pip install -r requirements.txt
Environment Variables
Create a .env file in the project root.
Copy code

OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
Running the Application
Run the Streamlit application:
Copy code

python -m streamlit run interactive_assistant/app.py
Then open:
Copy code

http://localhost:8501
Example Workflow
Enter a research topic such as:
Copy code

Natural Language Processing
The system generates a structured academic summary.
Upload a research paper PDF to receive a summarized version.
Ask follow-up questions like:
Copy code

What are the main challenges mentioned in this research?
The system answers using only the previously generated research context.
Challenges Faced
Controlling hallucinations in LLM outputs
Maintaining research context across follow-up questions
Coordinating multi-agent workflows using LangGraph
Integrating multiple APIs and managing environment variables
Implementing multi-chat session memory in Streamlit
Future Improvements
Multi-paper comparison
Citation extraction
Research trend visualization
Cloud deployment
Semantic search for research papers
License
This project is for educational and research purposes
