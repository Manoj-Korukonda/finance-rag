from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def create_vectorstore(chunks):
    print("🔄 Creating embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("📦 Building FAISS index...")
    db = FAISS.from_documents(chunks, embeddings)

    db.save_local("faiss_index")

    print("✅ FAISS index saved!")

    return db


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
    )
    return db