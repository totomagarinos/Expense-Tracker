import argparse

import argparse, json, os
from datetime import datetime

EXPENSES_FILE = "expenses.json"


def load_expenses():
  if os.path.exists(EXPENSES_FILE):
    with open(EXPENSES_FILE, "r") as f:
      return json.load(f)
  else:
    with open(EXPENSES_FILE, "w") as f:
      json.dump([], f)
    return []


def save_expenses(expenses):
  with open(EXPENSES_FILE, "w") as f:
    json.dump(expenses, f, indent=2)


def add_expense(description: str, amount: int):
  expenses = load_expenses()
  id = len(expenses) + 1
  date = datetime.now().strftime("%d/%m/%Y")

  expense = {
    "id": id,
    "date": date,
    "updated_at": date,
    "description": description,
    "amount": amount,
  }

  expenses.append(expense)
  save_expenses(expenses)
  print(f"Expense added successfully (ID: {id}).")


def update_expense(id, description:str=None, amount:float=None):
  expenses = load_expenses()
  date = datetime.now().strftime("%d/%m/%Y")
  
  for expense in expenses:
    if expense["id"] == id:
      expense["updated_at"] = date

      if description is not None and amount is not None:
        expense["description"] = description
        expense["amount"] = amount
        print(f"Expense {id} updated successfully.")
        break
      elif description is not None or amount is not None:
        if description is not None:
          expense["description"] = description
        else:
          expense["amount"] = amount
        print(f"Expense {id} updated successfully.")
        break
      elif description is None and amount is None:
        print("Please provide at least a description or an amount of the expense.")
        break
  else:
    print(f"Expense with ID: {id} not found.")
  save_expenses(expenses)


def delete_expense(id):
  expenses = load_expenses()

  for expense in expenses:
    if expense["id"] == id:
      expenses.remove(expense)
      save_expenses(expenses)
      print(f"Expense with ID: {id} deleted.")
      break
  else:
    print(f"Expense with ID: {id} not found.")

  for i, expense in enumerate(expenses, 1):
    expense["id"] = i
  save_expenses(expenses)


def list_expenses():
  expenses = load_expenses()

  if not expenses:
    print(f"No expenses found.")

  print(f"{'ID':<5} {'Date':<24} {'Description':<31} {'Amount':<5}")
  print('-' * 100)

  for expense in expenses:
    print(
      f'{expense["id"]:<6}'
      f'{expense["date"]:<25}'
      f'{expense["description"]:<32}'
      f'${expense["amount"]:<5}'
    )


def view_summary(month=None):
  expenses = load_expenses()
  summary = 0

  if month is not None:
    if month > 0 and month < 13:
      for expense in expenses:
        date_str = expense["date"]
        date = datetime.strptime(date_str, '%d/%m/%Y')

        if date.month == month:
          summary += expense["amount"]
      print(f"Total expenses for month {month}: ${summary}.")
    else:
      print("Please enter a month between 1 and 12.")


  elif month is None:
    for expense in expenses:
      summary += expense["amount"]

    print(f"Total expenses: ${summary}")


def main():
  parser = argparse.ArgumentParser(description="CLI Expenses Tracker")
  subparsers = parser.add_subparsers(dest="command", help="Command to run")

  # Add expense
  add_parser = subparsers.add_parser("add", help="Add new expense")
  add_parser.add_argument("description", help="Expense description")
  add_parser.add_argument("amount", type=float, help="Expense amount")

  # Update expense
  update_parser = subparsers.add_parser("update", help="Update an expense")
  update_parser.add_argument("id", type=int, help="ID of the expense to update")
  update_parser.add_argument("--description", help="New expense description")
  update_parser.add_argument("--amount", type=float, help="New expense amount")

  # Delete expense
  delete_parser = subparsers.add_parser("delete", help="Delete an expense")
  delete_parser.add_argument("id", type=int, help="ID of the expense to delete")

  # List parser
  list_parser = subparsers.add_parser("list", help="List expenses")

  # View summary
  summary_parser = subparsers.add_parser("view-summary", help="View summary of all expenses")
  summary_parser.add_argument("--month", type=int, help="Month to filter the expense summary")


  args = parser.parse_args()

  if args.command == "add":
    add_expense(args.description, args.amount)
  elif args.command == "update":
    update_expense(args.id, args.description, args.amount)
  elif args.command == "delete":
    delete_expense(args.id)
  elif args.command == "list":
    list_expenses()
  elif args.command == "view-summary":
    view_summary(args.month)
  else:
    parser.print_help()

if __name__ == "__main__":
    main()