from gettext import translation
from test_transaction import transaction
import pytest

@pytest.fixture

def test_addTransaction():
    transaction = translation(":memory:") # database
    transaction.addTransaction(100, "category1", "2023-03-26", "description1")
    result = transaction.conn.execute("SELECT * FROM transactions").fetchall()
    assert len(result) == 1
    assert result[0][1] == 100
    assert result[0][2] == "category1"
    assert result[0][3] == "2023-03-26"
    assert result[0][4] == "description1"


def test_deleteTransaction():
    transaction = translation(":memory:")
    transaction.addTransaction(100, "category1", "2023-03-26", "description1")
    transaction.deleteTransaction(1)
    assert len(transaction.showTransactions()) == 0 


def test_summarizeDate():
    transaction.addTransaction(100, "category1", "2023-03-21", "description1")
    transaction.addTransaction(30, "category2", "2023-03-22", "description2")
    transaction.addTransaction(94, "category3", "2023-03-23", "description3")
    transaction.addTransaction(720, "category4", "2023-03-24", "description4")
    transaction.addTransaction(2708, "category5", "2023-03-25", "description5")

    summary = transaction.summarizeDate()
    assert sorted(summary.keys()) == ['2023-03-21', '2023-03-22', '2023-03-23', '2023-03-24', '2023-03-25' ]
    assert summary['2023-03-21'] == 100
    assert summary['2023-03-22'] == 30
    assert summary['2023-03-23'] == 94
    assert summary['2023-03-23'] == 720
    assert summary['2023-03-23'] == 2708
