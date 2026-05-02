from src.helper import get_answer

while True:
    query = input("Ask: ")

    if query.lower() == "exit":
        break

    answer = get_answer(query)
    print("Bot:", answer)
