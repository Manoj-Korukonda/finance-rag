from src.retriever import load_vectorstore
from src.llm import generate_answer

db = load_vectorstore()

def ask_question(query):
    docs = db.similarity_search(query, k=5)

    context = "\n\n".join([doc.page_content for doc in docs])

    answer = generate_answer(context, query)

    return answer, docs