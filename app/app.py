import sys
import os

# ✅ Fix: make src import work on Streamlit Cloud
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.pipeline import ask_question
from src.retriever import load_vectorstore
from src.build_index import create_vectorstore
from src.ingest import load_and_split

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Finance RAG Chatbot", layout="wide")

st.title("📊 Finance RAG Chatbot")

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "db_ready" not in st.session_state:
    st.session_state.db_ready = False

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

# -------------------------------
# BUILD VECTOR DB (ONLY ONCE)
# -------------------------------
if uploaded_file and not st.session_state.db_ready:
    with st.spinner("Processing PDF..."):
        # Save temp file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        docs = load_and_split("temp.pdf")
        create_vectorstore(docs)

        st.session_state.db_ready = True

    st.success("✅ PDF processed! You can now ask questions.")

# -------------------------------
# LOAD VECTORSTORE (ONLY ONCE)
# -------------------------------
if st.session_state.db_ready and "db_loaded" not in st.session_state:
    st.session_state.db = load_vectorstore()
    st.session_state.db_loaded = True

# -------------------------------
# CHAT DISPLAY
# -------------------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -------------------------------
# FIXED INPUT BAR (BOTTOM)
# -------------------------------
query = st.chat_input("Ask a question from the PDF...")

if query and st.session_state.db_ready:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_question(query, st.session_state.db)
            st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})

elif query and not st.session_state.db_ready:
    st.warning("⚠️ Please upload and process a PDF first.")