import json
from tinydb import TinyDB
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class ExpenseInput(BaseModel):
    """Schema for adding an expense entry"""
    user_request: str = Field(..., description="The original user request that led to this expense")
    category: str = Field(..., description="The main category for this expense (e.g., 'Food', 'Transport', 'Entertainment')")
    sub_category: str = Field(..., description="The specific sub-category within the main category")
    amount: float = Field(..., description="The monetary amount of the expense (must be positive)")
    date: str = Field(..., description="The date and time in DD-MM-YYYY-HH-MM format (e.g., '25-12-2024-14-30')")


@tool
def get_categories_subcategories() -> str:
    """Get category and subcategories options from tinydb"""
    db = TinyDB("category_db.json")
    table = db.table("categories")
    data = table.get(doc_id=1)
    db.close()
    mapping = dict(data or {})
    return json.dumps(mapping, ensure_ascii=False)


@tool
def add_expense(expense: ExpenseInput) -> str:
    """Add expense to tinydb with proper validation"""
    expense_data = expense.model_dump()

    if expense.amount <= 0:
        return json.dumps({"status": "error", "message": "amount must be a positive number"})

    try:
        from datetime import datetime
        datetime.strptime(expense.date, "%d-%m-%Y-%H-%M")
    except ValueError:
        return json.dumps({"status": "error", "message": "date must be in DD-MM-YYYY-HH-MM format"})

    db = TinyDB("expense_db.json")
    table = db.table("expenses")
    table.insert(expense_data)
    db.close()

    return json.dumps({"status": "success", "message": "Expense added successfully"})


