from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split(pdf_path):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    print(f"\n✅ Loaded {len(docs)} pages")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    print(f"✅ Created {len(chunks)} chunks")

    return chunks


# 🧠 What is if __name__ == "__main__"?

# Think of it as:

# 👉 “Run this part ONLY when I run this file directly”


if __name__ == "__main__":
    pdf_path = "data/infosys.pdf"

    chunks = load_and_split(pdf_path)

    print("\n📄 Sample chunk:\n")
    print(chunks[0].page_content[:500])