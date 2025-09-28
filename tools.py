import json
from tinydb import TinyDB


def get_categories_subcategories() -> str:
    """Get category and subcategories options from tinydb"""
    db = TinyDB("category_db.json")
    table = db.table("categories")
    data = table.get(doc_id=1)
    db.close()
    mapping = dict(data or {})
    return json.dumps(mapping, ensure_ascii=False)

def add_expense(expense_json: str) -> str:
    """Add expense to tinydb"""
    try:
        expense_data = json.loads(expense_json)
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "Invalid JSON format"})

    # Required fields validation
    required_fields = ["user_request", "category", "sub_category", "amount", "date"]
    for field in required_fields:
        if field not in expense_data:
            return json.dumps({"status": "error", "message": f"Missing required field: {field}"})

    # Type validation
    if not isinstance(expense_data["user_request"], str) or not expense_data["user_request"].strip():
        return json.dumps({"status": "error", "message": "user_request must be a non-empty string"})

    if not isinstance(expense_data["category"], str) or not expense_data["category"].strip():
        return json.dumps({"status": "error", "message": "category must be a non-empty string"})

    if not isinstance(expense_data["sub_category"], str):
        return json.dumps({"status": "error", "message": "sub_category must be a string"})

    try:
        amount = float(expense_data["amount"])
        if amount <= 0:
            return json.dumps({"status": "error", "message": "amount must be a positive number"})
        expense_data["amount"] = amount
    except (ValueError, TypeError):
        return json.dumps({"status": "error", "message": "amount must be a valid number"})

    # Date format validation (DD-MM-YYYY-HH-MM)
    if not isinstance(expense_data["date"], str):
        return json.dumps({"status": "error", "message": "date must be a string"})

    try:
        from datetime import datetime
        datetime.strptime(expense_data["date"], "%d-%m-%Y-%H-%M")
    except ValueError:
        return json.dumps({"status": "error", "message": "date must be in DD-MM-YYYY-HH-MM format"})

    # If all validations pass, insert into database
    db = TinyDB("expense_db.json")
    table = db.table("expenses")
    table.insert(expense_data)
    db.close()

    return json.dumps({"status": "success", "message": "Expense added successfully"})
