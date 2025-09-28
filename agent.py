from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from tools import add_expense

load_dotenv()

# define a system prompt variable
system_prompt = """
You are an expense tracker assistant. You are given a list of expenses and you need to process it using given tools and add it.
"""

agent = create_react_agent(
    model="gpt-4o-mini",
    tools=[add_expense],
    prompt=system_prompt,
)

def display_tool_interaction(messages):
    """Display tool calls and their responses in a clean format"""
    tool_calls = []
    tool_responses = []

    for message in messages:
        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append({
                    'function': tool_call['name'],
                    'args': tool_call['args'],
                    'id': tool_call['id']
                })
        elif hasattr(message, 'tool_call_id') and message.tool_call_id:
            tool_responses.append({
                'id': message.tool_call_id,
                'content': message.content,
                'tool_name': getattr(message, 'name', 'Unknown')
            })

    if tool_calls:
        print("\n🔧 Tool Interactions:")
        for i, (call, response) in enumerate(zip(tool_calls, tool_responses), 1):
            print(f"  {i}. Called: {call['function']}({call['args']})")
            print(f"     Response: {response['content']}")
        print()

def get_final_answer(messages):
    """Extract the final answer from the conversation"""
    for message in reversed(messages):
        if hasattr(message, 'type') and message.type == 'ai' and (not hasattr(message, 'tool_calls') or not message.tool_calls):
            return message.content
    return None