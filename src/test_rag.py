from src.pipeline import ask_question

if __name__ == "__main__":
    query = "What is Infosys revenue?"

    answer, docs = ask_question(query)

    print("\n🧠 Answer:\n")
    print(answer)

    print("\n📄 Sources:\n")
    for d in docs:
        print(f"Page: {d.metadata.get('page')}")