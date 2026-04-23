from agent.graph import build_graph

def run_chat():
    app = build_graph()

    state = {
        "user_input": "",
        "intent": None,
        "response": None,
        "name": None,
        "email": None,
        "platform": None
    }

    print("\n🤖 AutoStream AI Agent\n(Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break

        state["user_input"] = user_input

        state = app.invoke(state)

        print("Bot:", state["response"])


if __name__ == "__main__":
    run_chat()