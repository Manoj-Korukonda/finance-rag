import streamlit as st
import tempfile

from src.pipeline import ask_question
from src.ingest import load_and_split
from src.retriever import create_vectorstore
from src.llm import generate_answer

st.set_page_config(page_title="Finance RAG", layout="wide")

# ---------------------------
# CLEAN CSS (NO GAP + CHAT UI)
# ---------------------------
st.markdown("""
<style>

/* Reduce default spacing */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Chat container */
.chat-container {
    max-height: calc(100vh - 200px);
    overflow-y: auto;
    padding: 10px;
    margin-bottom: 80px;
}

/* Chat bubbles */
.user-msg {
    background-color: #DCF8C6;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    text-align: right;
}

.bot-msg {
    background-color: #F1F0F0;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    text-align: left;
}

/* Fixed input bar */
.input-box {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: white;
    padding: 10px;
    border-top: 1px solid #ccc;
    z-index: 999;
}

</style>
""", unsafe_allow_html=True)

st.title("📊 Finance RAG Chat")

# ---------------------------
# SESSION STATE
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "db" not in st.session_state:
    st.session_state.db = None

if "last_file" not in st.session_state:
    st.session_state.last_file = None

# ---------------------------
# CACHE PDF
# ---------------------------
@st.cache_resource
def process_pdf(file_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_bytes)
        file_path = tmp_file.name

    chunks = load_and_split(file_path)
    db = create_vectorstore(chunks)
    return db

# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload PDF", type="pdf")

if uploaded_file:
    if st.session_state.last_file != uploaded_file.name:

        with st.spinner("🔄 Processing PDF (only once)..."):
            db = process_pdf(uploaded_file.read())

        st.session_state.db = db
        st.session_state.last_file = uploaded_file.name
        st.session_state.history = []

        st.success("✅ PDF ready!")

# Divider (removes weird gap feel)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------
# CHAT DISPLAY
# ---------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for q, a, docs in st.session_state.history:
    st.markdown(f'<div class="user-msg">🧑 {q}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-msg">🤖 {a}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# FIXED INPUT (FORM)
# ---------------------------
st.markdown('<div class="input-box">', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])

    with col1:
        query = st.text_input("💬 Ask something...")

    with col2:
        send = st.form_submit_button("Send")

    if send and query:
        with st.spinner("🤖 Thinking..."):

            if st.session_state.db:
                docs = st.session_state.db.similarity_search(query, k=5)
                context = "\n\n".join([doc.page_content for doc in docs])
                answer = generate_answer(context, query)
            else:
                answer, docs = ask_question(query)

        st.session_state.history.append((query, answer, docs))

        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)