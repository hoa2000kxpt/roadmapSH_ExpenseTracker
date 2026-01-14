import pytest
from datetime import datetime
from expense_tracker.repository import ExpenseNotFoundError



def test_add_expense(repo):
    expense = repo.add("Lunch", 20, "food")

    assert expense["id"] == 1
    assert expense["description"] == "Lunch"
    assert expense["amount"] == 20
    assert expense["category"] == "food"


def test_list_expenses(repo):
    repo.add("Lunch", 20, "food")
    repo.add("Dinner", 10, "food")

    expenses = repo.list()
    assert len(expenses) == 2


def test_get_expense(repo):
    expense = repo.add("Coffee", 5, "drink")
    fetched = repo.get(expense["id"])

    assert fetched["description"] == "Coffee"


def test_get_nonexistent_expense(repo):
    with pytest.raises(ExpenseNotFoundError):
        repo.get(999)


def test_update_expense(repo):
    expense = repo.add("Lunch", 20, "food")

    updated = repo.update(expense["id"], amount=25)

    assert updated["amount"] == 25


def test_update_nonexistent_expense(repo):
    with pytest.raises(ExpenseNotFoundError):
        repo.update(999, amount=10)


def test_delete_expense(repo):
    expense = repo.add("Lunch", 20, "food")
    repo.delete(expense["id"])

    assert repo.list() == []


def test_delete_nonexistent_expense(repo):
    with pytest.raises(ExpenseNotFoundError):
        repo.delete(999)


def test_filter_by_category(repo):
    repo.add("Lunch", 20, "food")
    repo.add("Taxi", 15, "transport")

    food = repo.filter_by_category("food")
    assert len(food) == 1
    assert food[0]["description"] == "Lunch"


def test_filter_by_month(repo):
    repo.add("Lunch", 20, "food")
    current_month = int(datetime.now().month)  # Get current month of the year

    expenses = repo.filter_by_month(current_month)
    assert len(expenses) == 1
