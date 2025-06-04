
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
    "description": description,
    "amount": amount,
  }

  expenses.append(expense)
  save_expenses(expenses)
  print(f"Expense added successfully (ID: {id}).")


def update_expense(id, description, amount):
  expenses = load_expenses()
  date = datetime.now().strftime("%d/%m/%Y")
  updated = False
  
  for expense in expenses:
    if expense["id"] == id:
      expense["date"] = f"{date} (updated)"
      expense["description"] = description
      expense["amount"] = amount
      updated = True
      break
  
  if updated:
    save_expenses(expenses)
    print(f"Expense {id} updated successfully.")
  else:
    print(f"Expense with ID: {id} not found.")


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
      f'{expense["amount"]:<5}'
    )


def view_summary():
  expenses = load_expenses()
  summary = 0

  for expense in expenses:
    summary += expense["amount"]
  
  print(f"Total expenses: ${summary}")


def view_month_summary(month):
  expenses = load_expenses()
  month_summary = 0

  for expense in expenses:
    date_str = expense["date"]
    date = datetime.strptime(date_str, '%d/%m/%Y')

    if date.month == month:
      month_summary += expense["amount"]

  print(f"Total expenses for month {month}: ${month_summary}.")


# add_expense("Esta es la expensa 1", 20)
# add_expense("Esta es la expensa 2", 20)
# add_expense("Esta es la expensa 3", 20)
# update_expense(2, "actualizando expensa 2", 34)
# delete_expense(4)
# list_expenses()
# view_summary()
# view_month_summary(10)