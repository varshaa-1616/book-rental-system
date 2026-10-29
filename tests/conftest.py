"""Shared fixtures for the Book Rental test suite.

We mock mysql.connector.connect globally so that importing the app modules
(book1, book2, book3, app) never attempts a real database connection.
"""
import sys
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Patch mysql.connector.connect BEFORE any app module is imported.
# This avoids the class-level DB.mydb = mysql.connector.connect(...) in book1.py
# and the masala('aaa') call at the bottom of book2.py from hitting a real DB.
# ---------------------------------------------------------------------------

_mock_connect = MagicMock()
_mock_connection = MagicMock()
_mock_cursor = MagicMock()
_mock_connect.return_value = _mock_connection
_mock_connection.cursor.return_value = _mock_cursor

_patcher = patch("mysql.connector.connect", _mock_connect)
_patcher.start()

# Now it's safe to import the Flask app
from app import app as flask_app  # noqa: E402


@pytest.fixture()
def client():
    """Yield a Flask test client with fresh mocks for each test."""
    flask_app.config["TESTING"] = True

    # Reset the mock so each test starts clean
    _mock_cursor.reset_mock()
    _mock_connection.reset_mock()
    _mock_cursor.fetchall.return_value = []
    _mock_cursor.__iter__ = MagicMock(return_value=iter([]))

    with flask_app.test_client() as c:
        yield c


@pytest.fixture()
def mock_cursor():
    """Expose the shared mock cursor for assertions / return-value setup."""
    return _mock_cursor


@pytest.fixture()
def mock_connection():
    """Expose the shared mock connection."""
    return _mock_connection

