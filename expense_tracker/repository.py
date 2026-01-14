import json
import os
from datetime import date
from typing import List, Dict

class ExpenseNotFoundError(Exception):
    pass

class ExpenseRepository:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            self._write({"expenses": [], "budgets": {}})

    # ---------- Internal helpers ----------
    def _read(self):
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def _next_id(self, expenses: List[Dict]) -> int:
        return max((e["id"] for e in expenses), default=0) + 1

    # ---------- CRUD operation ----------
    def add(self, description: str, amount: float, category: str) -> dict:
        data = self._read()

        expense = {
            "id": self._next_id(data["expenses"]),
            "description": description,
            "amount": amount,
            "category": category,
            "date": date.today().isoformat(),
        }

        data["expenses"].append(expense)
        self._write(data)
        return expense

    def get(self, expense_id: int) -> dict:
        for expense in self.list():
            if expense["id"] == expense_id:
                return expense
        raise ExpenseNotFoundError(f"Expense with ID {expense_id} not found")

    def list(self):
        return self._read()["expenses"]

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

    def set_budget(self, month: int, amount: float):
        data = self._load_raw_data()
        if "budget" not in data:
            data["budget"] = {}
        data["budget"][str(month)] = amount
        self._save_raw_data(data)

    def get_budget(self, month):
        return self._read()["budgets"].get(str(month))
