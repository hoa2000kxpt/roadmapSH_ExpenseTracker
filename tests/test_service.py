import pytest
from expense_tracker.service import ExpenseService
from expense_tracker.logger import get_logger

def test_add_expense(service):
    expense = service.add_expense("Lunch", 20, "food")

    assert expense["id"] == 1


def test_add_expense_validation(service):
    with pytest.raises(ValueError):
        service.add_expense("", 10, "food")

    with pytest.raises(ValueError):
        service.add_expense("Lunch", -5, "food")


def test_update_expense(service):
    expense = service.add_expense("Lunch", 20, "food")

    updated = service.update_expense(expense["id"], None, 30, None)

    assert updated["amount"] == 30


def test_update_invalid_amount(service):
    expense = service.add_expense("Lunch", 20, "food")

    with pytest.raises(ValueError):
        service.update_expense(expense["id"], None, -10, None)


def test_delete_expense(service):
    expense = service.add_expense("Lunch", 20, "food")

    service.delete_expense(expense["id"])
    assert service.list_expenses() == []


def test_list_expenses(service):
    service.add_expense("Lunch", 20, "food")
    service.add_expense("Taxi", 10, "transport")

    expenses = service.list_expenses()
    assert len(expenses) == 2


def test_list_expenses_by_category(service):
    service.add_expense("Lunch", 20, "food")
    service.add_expense("Taxi", 10, "transport")

    food = service.list_expenses("food")
    assert len(food) == 1
