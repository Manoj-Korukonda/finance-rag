from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(context, query):
    prompt = f"""
    You are a financial analyst assistant.

    Answer the question using ONLY the context provided.
    Be precise and structured.

    Rules:
    - If data is present, include numbers clearly
    - Add page references like (Page X)
    - If not found, say: "Not available in report"
    - Keep answer concise but informative

    Context:
    {context}

    Question:
    {query}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content