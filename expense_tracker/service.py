import csv
from typing import List, Tuple


class ExpenseService:
    def __init__(self, repo, logger):
        self.repo = repo
        self.logger = logger

    # ---------- Commands logic ----------
    def add_expense(self, description: str, amount: float, category: str):
        if not description.strip():
            raise ValueError("Description cannot be empty")
        if amount <= 0:
            raise ValueError("Amount must be positive")

        expense = self.repo.add(description, amount, category)
        self.logger.info(f"Added expense {expense["id"]}")
        return expense

    def update_expense(
            self,
            expense_id: int,
            description: str | None,
            amount: float | None,
            category: str | None,
    ):
        if amount is not None and amount <= 0:
            raise ValueError("Amount must be positive")

        updated = self.repo.update(
            expense_id,
            description=description,
            amount=amount,
            category=category,
        )
        self.logger.info(f"Updated expense {expense_id}")
        return updated

    def delete_expense(self, expense_id: int):
        self.repo.delete(expense_id)
        self.logger.info(f"Expense deleted: {expense_id}")

    # ---------- Queries ----------
    def list_expenses(self, category=None) -> List[dict]:
        if category:
            return self.repo.filter_by_category(category)
        return self.repo.list()

    def summary(self, month: int | None = None) -> Tuple[float, float | None, bool]:
        expenses = (
            self.repo.filter_by_month(month)
            if month
            else self.repo.list()
        )

        total = sum(e["amount"] for e in expenses)
        budget = self.repo.get_budget(month) if month else None
        exceeded = budget is not None and total > budget

        return total, budget, exceeded

    def export_csv(self, filepath):
        expenses = self.repo.list()
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "date", "description", "amount", "category"]
            )
            writer.writeheader()
            writer.writerows(expenses)
