import json
from pathlib import Path
from datetime import date
from typing import List, Dict
from expense_tracker.models import Expense
from expense_tracker.logger import get_logger

logger = get_logger()

class ExpenseNotFoundError(Exception):
    pass

class ExpenseRepository:
    def __init__(self, filepath="data/expenses.json"):
        self.file_path = Path(filepath)
        self.file_path.parent.mkdir(exist_ok=True)


        if not self.file_path.exists():
            self._write([])

    # ---------- Internal helpers ----------
    def _read(self) -> list:
        if not self.file_path.exists():
            return []

        raw = self.file_path.read_text().strip()

        if not raw:
            return []

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError("Corrupted expenses.json file")

        if not isinstance(data, list):
            raise ValueError("Invalid data format: expected a list")

        return data

    def _write(self, data: list):
        self.file_path.write_text(json.dumps(data, indent=2))

    def _next_id(self, data: list) -> int:
        return max((expense["id"] for expense in data), default=0) + 1

    # ---------- CRUD operation ----------
    def add(self, description: str, amount: float, category: str) -> dict:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        data = self._read()
        expense = Expense(
            expense_id=self._next_id(data),
            description=description,
            amount=amount,
            category=category,
        )

        data.append(expense.to_dict())
        self._write(data)

        logger.info("Expense added", extra=expense.to_dict())
        return expense.to_dict()

    def get(self, expense_id: int) -> dict:
        for expense in self.list():
            if expense["id"] == expense_id:
                return expense
        raise ExpenseNotFoundError(f"Expense with ID {expense_id} not found")

    def list(self):
        return self._read()

    def delete(self, expense_id):
        data = self._read()
        expenses = data["expenses"]
        updated = [e for e in expenses if e["id"] != expense_id]

        if len(updated) == len(expenses):
            raise ExpenseNotFoundError(f"Expense {expense_id} not found")

        data["expenses"] = updated
        self._write(data)

    def update(self, expense_id: int, **fields) -> Dict:
        data = self._read()
        for expense in data["expenses"]:
            if expense["id"] == expense_id:
                for key, value in fields.items():
                    if value is not None:
                        expense[key] = value
                self._write(data)

                logger.info("Expense updated", extra=expense)
                return expense

        raise ExpenseNotFoundError(f"Expense {expense_id} not found")

    # ---------- Queries ----------
    def filter_by_category(self, category: str) -> List[Dict]:
        return [e for e in self.list() if e["category"] == category]

    def filter_by_month(self, month: int) -> List[Dict]:
        return [
            e for e in self.list()
            if int(e["date"].split("-")[1]) == month
        ]

    # def set_budget(self, month: int, amount: float):
    #     data = self._read()
    #     data["budgets"][str(month)] = amount
    #     self._write(data)
    #
    # def get_budget(self, month):
    #     return self._read()["budgets"].get(str(month))
