import argparse

import argparse, json, os
from datetime import datetime

SALES_FILE = "sales.json"


def load_sales():
  if os.path.exists(SALES_FILE):
    with open(SALES_FILE, "r") as f:
      return json.load(f)
  else:
    with open(SALES_FILE, "w") as f:
      json.dump([], f)
    return []


def save_sales(sales):
  with open(SALES_FILE, "w") as f:
    json.dump(sales, f, indent=2)


def add_sale(description: str, amount: int):
  sales = load_sales()
  id = len(sales) + 1
  date = datetime.now().strftime("%d/%m/%Y")

  sale = {
    "id": id,
    "date": date,
    "updated_at": date,
    "description": description,
    "amount": amount,
  }

  sales.append(sale)
  save_sales(sales)
  print(f"Sale added successfully (ID: {id}).")


def update_sale(id, description:str=None, amount:float=None):
  sales = load_sales()
  date = datetime.now().strftime("%d/%m/%Y")
  
  for sale in sales:
    if sale["id"] == id:
      sale["updated_at"] = date

      if description is not None and amount is not None:
        sale["description"] = description
        sale["amount"] = amount
        print(f"Sale {id} updated successfully.")
        break
      elif description is not None or amount is not None:
        if description is not None:
          sale["description"] = description
        else:
          sale["amount"] = amount
        print(f"Sale {id} updated successfully.")
        break
      elif description is None and amount is None:
        print("Please provide at least a description or an amount of the sale.")
        break
  else:
    print(f"Sale with ID: {id} not found.")
  save_sales(sales)


def delete_sale(id):
  sales = load_sales()

  for sale in sales:
    if sale["id"] == id:
      sales.remove(sale)
      save_sales(sales)
      print(f"Sale with ID: {id} deleted.")
      break
  else:
    print(f"Sale with ID: {id} not found.")

  for i, sale in enumerate(sales, 1):
    sale["id"] = i
  save_sales(sales)


def list_sales():
  sales = load_sales()

  if not sales:
    print(f"No sales found.")

  print(f"{'ID':<5} {'Date':<24} {'Updated at':<24} {'Description':<31} {'Amount':<5}")
  print('-' * 100)

  for sale in sales:
    print(
      f'{sale["id"]:<6}'
      f'{sale["date"]:<25}'
      f'{sale["updated_at"]:<25}'
      f'{sale["description"]:<32}'
      f'${sale["amount"]:<5}'
    )


def view_summary(month=None):
  sales = load_sales()
  summary = 0

  if month is not None:
    if month > 0 and month < 13:
      for sale in sales:
        date_str = sale["date"]
        date = datetime.strptime(date_str, '%d/%m/%Y')

        if date.month == month:
          summary += sale["amount"]
      print(f"Total sales for month {month}: ${summary}.")
    else:
      print("Please enter a month between 1 and 12.")


  elif month is None:
    for sale in sales:
      summary += sale["amount"]

    print(f"Total sales: ${summary}")


def main():
  parser = argparse.ArgumentParser(description="CLI Sales Tracker")
  subparsers = parser.add_subparsers(dest="command", help="Command to run")

  # Add sale
  add_parser = subparsers.add_parser("add", help="Add new sale")
  add_parser.add_argument("description", help="Sale description")
  add_parser.add_argument("amount", type=float, help="Sale amount")

  # Update sale
  update_parser = subparsers.add_parser("update", help="Update an sale")
  update_parser.add_argument("id", type=int, help="ID of the sale to update")
  update_parser.add_argument("--description", help="New sale description")
  update_parser.add_argument("--amount", type=float, help="New sale amount")

  # Delete sale
  delete_parser = subparsers.add_parser("delete", help="Delete an sale")
  delete_parser.add_argument("id", type=int, help="ID of the sale to delete")

  # List parser
  list_parser = subparsers.add_parser("list", help="List sales")

  # View summary
  summary_parser = subparsers.add_parser("summary", help="View summary of all sales")
  summary_parser.add_argument("--month", type=int, help="Month to filter the sale summary")


  args = parser.parse_args()

  if args.command == "add":
    add_sale(args.description, args.amount)
  elif args.command == "update":
    update_sale(args.id, args.description, args.amount)
  elif args.command == "delete":
    delete_sale(args.id)
  elif args.command == "list":
    list_sales()
  elif args.command == "summary":
    view_summary(args.month)
  else:
    parser.print_help()

if __name__ == "__main__":
    main()