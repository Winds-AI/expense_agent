from langgraph.prebuilt import create_react_agent
from ..common import display_tool_interaction


def build_agent():
    system_prompt = (
        "You are a simple echo assistant. Repeat the user's message back in a friendly way. "
        "Keep responses brief."
    )
    # no tools for this simple agent
    return create_react_agent(
        model="gpt-4o-mini",
        tools=[],
        prompt=system_prompt,
    )


def get_final_answer(messages):
    for message in reversed(messages):
        if hasattr(message, 'type') and message.type == 'ai' and (not hasattr(message, 'tool_calls') or not message.tool_calls):
            return message.content
    return None


