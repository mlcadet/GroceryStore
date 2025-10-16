import pytest
from unittest.mock import MagicMock
from backend.uom_dao import UOMDAO


def make_mock_connection():
    cursor = MagicMock()
    # cursor.execute doesn't need to return anything
    # cursor.lastrowid will simulate an inserted id
    cursor.lastrowid = 42
    # cursor.rowcount will simulate deletion result
    cursor.rowcount = 1

    # context manager support
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = cursor
    mock_conn.cursor.return_value.__exit__.return_value = None
    return mock_conn, cursor


def test_insert_uom_happy_path():
    mock_conn, cursor = make_mock_connection()
    dao = UOMDAO(mock_conn)

    new_id = dao.insert_uom({'uom_name': 'kg'})

    # Ensure insert query executed and returned lastrowid
    cursor.execute.assert_called()
    assert new_id == 42


def test_insert_uom_missing_key_raises_value_error():
    mock_conn, cursor = make_mock_connection()
    dao = UOMDAO(mock_conn)

    with pytest.raises(ValueError):
        dao.insert_uom({'wrong_key': 'value'})


def test_delete_uom_returns_rowcount():
    mock_conn, cursor = make_mock_connection()
    dao = UOMDAO(mock_conn)

    rows_deleted = dao.delete_uom(5)
    cursor.execute.assert_called()
    assert rows_deleted == 1
