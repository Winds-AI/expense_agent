from agent import agent, display_tool_interaction, get_final_answer
from time import time

def main():
    print("🤖 Expense Tracker Agent Started!")
    print("Ask me about expenses or type 'bye' to exit.\n")

    conversation_history = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'bye':
            print("👋 Goodbye!")
            break

        if not user_input:
            continue

        # Add user message to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        print("Thinking...")

        start_time = time()
        result = agent.invoke({"messages": conversation_history})
        end_time = time()

        # Update conversation history with agent response
        conversation_history = result["messages"]

        # Display tool interactions if any
        display_tool_interaction(result["messages"])

        # Get and display final answer
        final_answer = get_final_answer(result["messages"])
        if final_answer:
            print(f"🤖 Agent: {final_answer}")
        else:
            print("🤖 Agent: I couldn't process that request.")

        print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
        print()

if __name__ == "__main__":
    main()
