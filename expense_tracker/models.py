from datetime import datetime

# --- 1. Data Model ---
class Expense:
    def __init__(self, description: str, amount: float, category: str = "General", date: str = None, expense_id: int = None):
        self.expense_id = expense_id
        self.description = description
        self.amount = amount
        self.category = category
        # Default to today if no date provided
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "id": self.expense_id,
            "date": self.date,
            "description": self.description,
            "amount": self.amount,
            "category": self.category
        }