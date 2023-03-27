from test_transaction import transaction
import sqlite3
import pytest

@pytest.fixture
def test_addTransaction():
    transaction.addTransaction(100, "category1", "2023-03-26", "description1")
    assert len(transaction) == 1
    assert transaction[0]["amount"] == 100
    assert transaction[0]["category"] == "category1"
    assert transaction[0]["date"] == "2023-03-26"
    assert transaction[0]["description"] == "description1"


@pytest.fixture
def test_deleteTransaction():
    transaction.addTransaction(100, "category1", "2023-03-26", "description1")
    transactions = transaction.conn.execute(
        "SELECT * FROM transactions").fetchall()
    assert len(transactions) == 1
    # now delete from the database
    transaction.deleteTransaction(1)
    transactions = transaction.conn.execute(
        "SELECT * FROM transactions").fetchall()
    assert len(transactions) == 0


@pytest.fixture
def test_summarizeDate():
    transaction.addTransaction(100, "category1", "2023-03-21", "description1")
    transaction.addTransaction(30, "category2", "2023-03-22", "description2")
    transaction.addTransaction(94, "category3", "2023-03-23", "description3")
    transaction.addTransaction(720, "category4", "2023-03-24", "description4")
    transaction.addTransaction(2708, "category5", "2023-03-25", "description5")

    summary = transaction.summarizeDate()
    assert sorted(summary.keys()) == [
        '2023-03-21', '2023-03-22', '2023-03-23', '2023-03-24', '2023-03-25']
    assert summary['2023-03-21'] == 100
    assert summary['2023-03-22'] == 30
    assert summary['2023-03-23'] == 94
    assert summary['2023-03-23'] == 720
    assert summary['2023-03-23'] == 2708


@pytest.fixture
def test_summarizeMonth():
    transaction.addTransaction(100, "category1", "2023-01-21", "description1")
    transaction.addTransaction(30, "category2", "2023-02-22", "description2")
    transaction.addTransaction(94, "category3", "2023-03-23", "description3")
    transaction.addTransaction(720, "category4", "2023-04-24", "description4")
    transaction.addTransaction(2708, "category5", "2023-05-25", "description5")

    result = transaction.summarizeMonth(2, 2023)
    assert result == {'02-2022': 30}


@pytest.fixture
def test_summarizeYear():
    transaction.addTransaction(100, "category1", "2021-01-21", "description1")
    transaction.addTransaction(30, "category2", "2022-02-22", "description2")
    transaction.addTransaction(94, "category3", "2023-03-23", "description3")
    transaction.addTransaction(720, "category4", "2023-04-24", "description4")
    transaction.addTransaction(2708, "category5", "2023-05-25", "description5")

    result = transaction.summarizeYear(2021)
    assert result == {'2021': 100}


@pytest.fixture
def test_summarizeCategory(transaction):
    transaction.addTransaction(100, "category1", "2021-01-21", "description1")
    transaction.addTransaction(30, "category2", "2022-02-22", "description2")
    transaction.addTransaction(94, "category3", "2023-03-23", "description1")
    transaction.addTransaction(720, "category4", "2023-04-24", "description2")
    transaction.addTransaction(2708, "category5", "2023-05-25", "description3")

    result = transaction.summarizeCategory()
    assert result == {"description1": 194,
                      "description2": 750, "description3": 2708}
