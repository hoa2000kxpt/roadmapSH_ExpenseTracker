import pytest
from expense_tracker.repository import ExpenseRepository
from expense_tracker.service import ExpenseService


class DummyLogger:
    def info(self, msg): pass
    def error(self, msg): pass


@pytest.fixture
def repo(tmp_path):
    file = tmp_path / "expenses.json"
    file.write_text('{"expenses": [], "budgets": {}}')
    return ExpenseRepository(str(file))


@pytest.fixture
def service(repo):
    return ExpenseService(repo, DummyLogger())
