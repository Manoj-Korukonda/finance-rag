from src.llm import generate_answer

def ask_question(query, db):
    docs = db.similarity_search(query, k=5)
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
    answer = generate_answer(context, query)
    
    return answer