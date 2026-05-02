from src.ingest import load_and_split
from src.retriever import create_vectorstore

if __name__ == "__main__":
    pdf_path = "data/infosys.pdf"

    chunks = load_and_split(pdf_path)

    db = create_vectorstore(chunks)