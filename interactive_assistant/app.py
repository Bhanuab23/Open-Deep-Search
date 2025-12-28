import sys
import os
import uuid
import streamlit as st
from pypdf import PdfReader

# -------------------------------------------------
# Add project root to PYTHONPATH
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend import route_user_input

# -------------------------------------------------
# Utility: Extract PDF Text
# -------------------------------------------------
def extract_pdf_text(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Research Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Research Assistant")
st.caption(
    "Research topics • PDF & URL summarization • General Q&A"
)

# -------------------------------------------------
# Chat State (Multi-chat)
# -------------------------------------------------
if "chats" not in st.session_state:
    first_chat_id = str(uuid.uuid4())
    st.session_state.chats = {
        first_chat_id: {
            "title": "New Chat",
            "messages": [],
            "research_context": None,
            "source_type": None,
            "summary_length": "Short"
        }
    }
    st.session_state.active_chat_id = first_chat_id

if "rename_chat_id" not in st.session_state:
    st.session_state.rename_chat_id = None

active_chat = st.session_state.chats[st.session_state.active_chat_id]

# -------------------------------------------------
# Sidebar: History / Settings
# -------------------------------------------------
with st.sidebar:
    tab_history, tab_settings = st.tabs(["🕘 History", "⚙️ Settings"])

    # =========================
    # HISTORY TAB
    # =========================
    with tab_history:
        st.caption("Your conversations")

        if st.button("➕ New Chat", use_container_width=True):
            new_id = str(uuid.uuid4())
            st.session_state.chats[new_id] = {
                "title": "New Chat",
                "messages": [],
                "research_context": None,
                "source_type": None,
                "summary_length": "Short"
            }
            st.session_state.active_chat_id = new_id
            st.session_state.rename_chat_id = None
            st.rerun()

        st.markdown("---")

        # ✅ captions AFTER divider (as requested)
        st.caption("Tap ✏️ to rename a chat")
        st.caption("Tap 🗑️ to delete a chat")

        for chat_id, chat in list(st.session_state.chats.items()):
            is_active = chat_id == st.session_state.active_chat_id

            # One clean row per chat
            col1, col2, col3 = st.columns([6, 1, 1])

            # ---- Chat title (open chat) ----
            with col1:
                if st.session_state.rename_chat_id == chat_id:
                    new_title = st.text_input(
                        "Rename chat",
                        value=chat["title"],
                        key=f"rename_input_{chat_id}"
                    )
                    if new_title.strip():
                        chat["title"] = new_title.strip()
                else:
                    label = chat["title"]
                    if is_active:
                        label = "➡️ " + label

                    if st.button(
                        label,
                        key=f"open_{chat_id}",
                        use_container_width=True
                    ):
                        st.session_state.active_chat_id = chat_id
                        st.session_state.rename_chat_id = None
                        st.rerun()

            # ---- Rename icon ----
            with col2:
                if st.button("✏️", key=f"rename_{chat_id}"):
                    st.session_state.rename_chat_id = chat_id
                    st.rerun()

            # ---- Delete icon ----
            with col3:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    del st.session_state.chats[chat_id]

                    if st.session_state.chats:
                        st.session_state.active_chat_id = next(
                            iter(st.session_state.chats)
                        )
                    else:
                        new_id = str(uuid.uuid4())
                        st.session_state.chats[new_id] = {
                            "title": "New Chat",
                            "messages": [],
                            "research_context": None,
                            "source_type": None,
                            "summary_length": "Short"
                        }
                        st.session_state.active_chat_id = new_id

                    st.session_state.rename_chat_id = None
                    st.rerun()

    # =========================
    # SETTINGS TAB
    # =========================
    with tab_settings:
        assistant_mode = st.radio(
            "Assistant Mode",
            ["Research Assistant", "General Assistant"]
        )

        active_chat["summary_length"] = st.selectbox(
            "Summary Length",
            ["Short", "Long"],
            index=0 if active_chat["summary_length"] == "Short" else 1
        )

        st.markdown("### 📄 Upload Research Paper")
        uploaded_pdf = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

# -------------------------------------------------
# Chat Display
# -------------------------------------------------
for message in active_chat["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------
# User Input
# -------------------------------------------------
user_input = st.chat_input(
    "Ask a research topic, upload a paper, paste a paper URL, or ask a question..."
)

if user_input is not None:
    user_input = user_input.strip()

    if not user_input:
        st.info(
            "ℹ️ Please enter a research topic, a general question, "
            "upload a PDF, or paste a research paper URL to continue."
        )
    else:
        active_chat["messages"].append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        pdf_text = extract_pdf_text(uploaded_pdf) if uploaded_pdf else None

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = route_user_input(
                    user_input=user_input,
                    session=active_chat,
                    pdf_text=pdf_text,
                    mode=assistant_mode
                )
                st.markdown(response)

        active_chat["messages"].append(
            {"role": "assistant", "content": response}
        )

        if active_chat["title"] == "New Chat":
            active_chat["title"] = user_input[:40]
