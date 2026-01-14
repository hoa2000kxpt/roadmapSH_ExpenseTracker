import argparse
from repository import ExpenseRepository
from service import ExpenseService
from logger import get_logger
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "expenses.json"

def main():
    parser = argparse.ArgumentParser(prog="expense-tracker")
    sub = parser.add_subparsers(dest="command")

    # Add command
    add = sub.add_parser("add")
    add.add_argument("--description", required=True)
    add.add_argument("--amount", type=float, required=True)
    add.add_argument("--category", default="general")

    # Update command
    update = sub.add_parser("update")
    update.add_argument("--id", type=int, required=True)
    update.add_argument("--description")
    update.add_argument("--amount", type=float)
    update.add_argument("--category")

    # Delete command
    delete = sub.add_parser("delete")
    delete.add_argument("--id", type=int, required=True)

    # Summary command
    summary = sub.add_parser("summary")
    summary.add_argument("--month", type=int)

    # List command
    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--category")

    # Budget command
    budget = sub.add_parser("set-budget")
    budget.add_argument("--month", type=int, required=True)
    budget.add_argument("--amount", type=float, required=True)

    # Export command
    export = sub.add_parser("export")
    export.add_argument("--file", required=True)

    args = parser.parse_args()
    logger = get_logger()
    repo = ExpenseRepository(DATA_FILE)
    service = ExpenseService(repo, logger)

    try:
        if args.command == "add":
            e = service.add_expense(args.description, args.amount, args.category)
            print(f"Expense added successfully (ID: {e['id']})")

        elif args.command == "update":
            service.update_expense(args.id, args.description, args.amount, args.category)
            print("Expense updated successfully")

        elif args.command == "delete":
            service.delete_expense(args.id)
            print("Expense deleted successfully")

        elif args.command == "list":
            expenses = service.list_expenses(args.category)
            print("ID  Date        Description  Amount  Category")
            for e in expenses:
                print(
                    f"{e['id']}  {e['date']}  {e['description']}  "
                    f"${e['amount']}  {e['category']}"
                )

        elif args.command == "summary":
            total, budget, warning = service.summary(args.month)
            print(f"Total expenses: ${total}")
            if budget:
                print(f"Budget: ${budget}")
            if warning:
                print("⚠ WARNING: Budget exceeded!")

        elif args.command == "set-budget":
            repo.set_budget(args.month, args.amount)
            print("Budget set successfully")

        elif args.command == "export":
            service.export_csv(args.file)
            print("Expenses exported successfully")

    except Exception as e:
        logger.error(str(e))
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
