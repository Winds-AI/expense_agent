from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from .tools import add_expense, get_categories_subcategories
from ..common import display_tool_interaction
import time


def build_agent():
    load_dotenv()

    system_prompt = f"""
You are an expense tracker assistant. 
Your job is to assist user to manage all things related to their expenses. 
User is indian so languages that user talks are: english, gujarati and gujlish.
reply in concise and english only.

For Adding Expense:
- Understand the user's request.
- Use the get_categories_subcategories tool to get the categories and subcategories.
- add expense using add_expense tool with the relevant category and subcategory, for time use current time: {time.strftime("%Y-%m-%d %H:%M:%S")} if not given.
"""

    return create_react_agent(
        model="gpt-4o-mini",
        tools=[add_expense, get_categories_subcategories],
        prompt=system_prompt,
    )


def get_final_answer(messages):
    for message in reversed(messages):
        if hasattr(message, 'type') and message.type == 'ai' and (not hasattr(message, 'tool_calls') or not message.tool_calls):
            return message.content
    return None


