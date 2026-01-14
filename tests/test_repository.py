import pytest
from datetime import datetime
import json
from expense_tracker.repository import ExpenseRepository
from expense_tracker.repository import ExpenseNotFoundError

@pytest.fixture
def repo(tmp_path):
    # tmp_path is a built-in pytest fixture that provides a temporary directory unique to this test invocation

    # 1. Create a path to a temporary JSON file
    test_file = tmp_path / "test_expenses.json"

    # 2. Initialize the repository with this temporary file
    repository = ExpenseRepository(filepath=test_file)

    # 3. Return the repository instance to the test function
    return repository

def test_add_expense(repo):
    # This now uses the fresh temporary file from the fixture above
    expense = repo.add("Lunch", 20, "food")

    # This assertion is now safe because the file is always empty at the start of the test
    assert expense["id"] == 1
    assert expense["description"] == "Lunch"
    assert expense["amount"] == 20
    assert expense["category"] == "food"

    with open(repo.file_path, "r") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["description"] == "Lunch"


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
