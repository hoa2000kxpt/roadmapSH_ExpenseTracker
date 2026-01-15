import pytest
from expense_tracker.repository import ExpenseRepository
from expense_tracker.service import ExpenseService

@pytest.fixture
def repo(tmp_path):
    # tmp_path is a built-in pytest fixture that provides a temporary directory unique to this test invocation

    # 1. Create a path to a temporary JSON file
    test_file = tmp_path / "test_expenses.json"

    # 2. Initialize the repository with this temporary file
    repository = ExpenseRepository(filepath=test_file)

    # 3. Return the repository instance to the test function
    return repository

@pytest.fixture
def service(repo):
    return ExpenseService(repo)