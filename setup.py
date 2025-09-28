"""
Setup script to initialize TinyDB databases for the expense tracker.
Run this once to create category_db.json and expense_db.json with default data.
"""

import os
from tinydb import TinyDB


def setup_databases():
    """Initialize TinyDB databases with default categories and empty expenses."""

    # Get database file paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    category_db_path = os.path.join(base_dir, "category_db.json")
    expense_db_path = os.path.join(base_dir, "expense_db.json")

    print("Setting up expense tracker databases...")

    # Initialize category database with default categories
    category_db = TinyDB(category_db_path)
    category_table = category_db.table("categories")

    # Default categories and subcategories
    default_categories = {
        "Food": ["Snacks", "lunch", "dinner", "late_Night"],
        "Entertainment": ["movie"],
        "PG": ["Rent", "AC_Bill"],
        "Transportation": ["Auto"],
        "Shopping": ["Grocery", "Clothes", "Electronics", "Books"],
    }

    # Only insert if the table is empty
    if not category_table.get(doc_id=1):
        category_table.insert(default_categories)
        print(f"✅ Created {category_db_path} with default categories:")
        for category, subcategories in default_categories.items():
            print(f"   - {category}: {', '.join(subcategories)}")
    else:
        print(f"⚠️  {category_db_path} already exists, skipping category setup.")

    category_db.close()

    # Initialize expense database (empty)
    expense_db = TinyDB(expense_db_path)
    expense_table = expense_db.table("expenses")

    # Just ensure the table exists
    expense_table.insert({})  # Insert empty document to create table
    expense_table.remove(doc_ids=[1])  # Remove the empty document

    print(f"✅ Created {expense_db_path} for storing expenses (currently empty).")

    expense_db.close()

    print("\n🎉 Setup complete! Your expense tracker is ready to use.")
    print(f"📁 Database files saved in: {base_dir}")


if __name__ == "__main__":
    setup_databases()
