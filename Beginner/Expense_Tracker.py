import argparse
import json
from datetime import datetime
from pathlib import Path

# File to store expenses
EXPENSE_FILE = Path("expenses.json")

# Initialize file if it doesn't exist
def init_expense_file():
    if not EXPENSE_FILE.exists():
        with open(EXPENSE_FILE, 'w') as f:
            json.dump([], f)

# Load expenses from file
def load_expenses():
    with open(EXPENSE_FILE, 'r') as f:
        return json.load(f)

# Save expenses to file
def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

# Add an expense
def add_expense(description, amount):
    expenses = load_expenses()
    expense_id = len(expenses) + 1
    expense = {
        "id": expense_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense_id})")

# Update an expense
def update_expense(expense_id, description=None, amount=None):
    expenses = load_expenses()
    for expense in expenses:
        if expense["id"] == expense_id:
            if description:
                expense["description"] = description
            if amount:
                expense["amount"] = amount
            save_expenses(expenses)
            print("Expense updated successfully")
            return
    print("Expense ID not found")

# Delete an expense
def delete_expense(expense_id):
    expenses = load_expenses()
    updated_expenses = [e for e in expenses if e["id"] != expense_id]
    if len(updated_expenses) < len(expenses):
        save_expenses(updated_expenses)
        print("Expense deleted successfully")
    else:
        print("Expense ID not found")

# List all expenses
def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.")
        return
    print(f"{'ID':<4} {'Date':<12} {'Description':<20} {'Amount':<10}")
    for e in expenses:
        print(f"{e['id']:<4} {e['date']:<12} {e['description']:<20} ${e['amount']:<10}")

# Show summary of expenses
def show_summary(month=None):
    expenses = load_expenses()
    if month:
        month_str = f"{month:02d}"
        filtered_expenses = [e for e in expenses if e["date"].startswith(f"2024-{month_str}")]
        total = sum(e["amount"] for e in filtered_expenses)
        print(f"Total expenses for {datetime.strptime(month_str, '%m').strftime('%B')}: ${total}")
    else:
        total = sum(e["amount"] for e in expenses)
        print(f"Total expenses: ${total}")

# Main function
def main():
    init_expense_file()
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True, help="Description of the expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount of the expense")

    # Update command
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", type=int, required=True, help="ID of the expense to update")
    update_parser.add_argument("--description", help="Updated description")
    update_parser.add_argument("--amount", type=float, help="Updated amount")

    # Delete command
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True, help="ID of the expense to delete")

    # List command
    subparsers.add_parser("list")

    # Summary command
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", type=int, help="Month (1-12) for monthly summary")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        show_summary(args.month)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
