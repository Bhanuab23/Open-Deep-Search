import sys
import os

# Add project root to PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend import route_user_input
from pypdf import PdfReader

def extract_pdf_text(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

import streamlit as st

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Research Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Research Assistant")
st.caption(
    "Research-topic summarization • Paper Q&A • PDF & URL support • Web Q&A"
)

# -----------------------------------
# Session Memory (ChatGPT-style)
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "research_context" not in st.session_state:
    st.session_state.research_context = None

if "source_type" not in st.session_state:
    st.session_state.source_type = None  # topic / pdf / url / general

if "summary_length" not in st.session_state:
    st.session_state.summary_length = "Short"

# -----------------------------------
# Sidebar Controls
# -----------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    # 🔁 Assistant Mode Selector (NEW)
    st.session_state.assistant_mode = st.radio(
        "Assistant Mode",
        ["Research Assistant", "General Assistant"],
        help="Use Research mode for papers & summaries, General mode for normal questions"
    )

    # 📏 Summary length (only relevant for research mode)
    st.session_state.summary_length = st.selectbox(
        "Summary Length",
        ["Short", "Long"]
    )

    # 🆕 New chat
    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.session_state.research_context = None
        st.session_state.source_type = None
        st.rerun()

    st.markdown("---")

    # 📄 PDF upload (only useful in Research mode)
    st.markdown("### 📄 Upload Research Paper (PDF)")
    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

# -----------------------------------
# Chat Display
# -----------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------
# User Input
# -----------------------------------
user_input = st.chat_input(
    "Ask a research topic, upload a paper, paste a paper URL, or ask a question..."
)

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Handle PDF if uploaded
    pdf_text = None
    if uploaded_pdf:
        pdf_text = extract_pdf_text(uploaded_pdf)

    # Call backend router
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = route_user_input(
                user_input=user_input,
                session=st.session_state,
                pdf_text=pdf_text,
                mode=st.session_state.assistant_mode
            )
            st.markdown(response)

    # Store assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
