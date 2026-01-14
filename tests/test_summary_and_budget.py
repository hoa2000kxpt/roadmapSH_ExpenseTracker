from datetime import datetime

def test_summary_all(service):
    service.add_expense("Lunch", 20, "food")
    service.add_expense("Dinner", 10, "food")

    total, budget, exceeded = service.summary()

    assert total == 30
    assert budget is None
    assert exceeded is False


def test_summary_month(service):
    service.add_expense("Lunch", 20, "food")
    current_month = datetime.now().month

    total, _, _ = service.summary(current_month)
    assert total == 20


# def test_budget_not_exceeded(service):
#     service.repo.set_budget(8, 100)
#
#     service.add_expense("Lunch", 30, "food")
#
#     total, budget, exceeded = service.summary(8)
#
#     assert total == 30
#     assert budget == 100
#     assert exceeded is False
#
#
# def test_budget_exceeded(service):
#     service.repo.set_budget(8, 50)
#
#     service.add_expense("Lunch", 30, "food")
#     service.add_expense("Dinner", 30, "food")
#
#     total, budget, exceeded = service.summary(8)
#
#     assert total == 60
#     assert budget == 50
#     assert exceeded is True
