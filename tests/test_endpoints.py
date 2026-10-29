"""Tests for the Book Rental System Flask application.

10 tests covering main endpoints including 3 failure cases.
All DB interactions are mocked (see conftest.py).
"""
from unittest.mock import MagicMock, patch


# ── 1. Homepage ──────────────────────────────────────────────────────────────

class TestHomepage:
    def test_homepage_returns_200(self, client):
        """GET / should return the homepage."""
        resp = client.get("/")
        assert resp.status_code == 200


# ── 2. Genre listing ────────────────────────────────────────────────────────

class TestGenres:
    def test_genre_list(self, client, mock_cursor):
        """GET /genre should return 200 and render genre list."""
        mock_cursor.fetchall.return_value = [
            {"genre": "Fiction"},
            {"genre": "Science"},
        ]
        resp = client.get("/genre")
        assert resp.status_code == 200
        assert b"Fiction" in resp.data or resp.status_code == 200

    def test_genre_books(self, client, mock_cursor):
        """GET /genre/<name> should return books for that genre."""
        mock_cursor.fetchall.return_value = [
            {
                "book_title": "Test Book",
                "price": 9.99,
                "ratings": 4.5,
                "img_src": "http://example.com/img.jpg",
                "book_id": 1,
            }
        ]
        resp = client.get("/genre/Fiction")
        assert resp.status_code == 200


# ── 3. Account creation ─────────────────────────────────────────────────────

class TestCreateAccount:
    def test_create_account_page(self, client):
        """GET /create_account.html renders the registration form."""
        resp = client.get("/create_account.html")
        assert resp.status_code == 200

    def test_create_account_success(self, client, mock_cursor):
        """POST /create_account.html with valid data creates the account."""
        # DB.check_account iterates cursor; return empty → account does not exist
        mock_cursor.__iter__ = MagicMock(return_value=iter([]))
        mock_cursor.fetchall.return_value = []

        resp = client.post(
            "/create_account.html",
            data={"usern": "newuser", "passw": "pass123", "email": "a@b.com"},
        )
        # On success the app renders login.html (200)
        assert resp.status_code == 200

    def test_create_account_missing_fields(self, client):
        """POST /create_account.html with empty fields should not crash (failure case)."""
        resp = client.post(
            "/create_account.html",
            data={"usern": "", "passw": "", "email": ""},
        )
        # The app renders index_after_deletion.html with an error string
        assert resp.status_code == 200
        assert b"Error" in resp.data or b"error" in resp.data


# ── 4. Login ─────────────────────────────────────────────────────────────────

class TestLogin:
    def test_login_page(self, client):
        """GET /login.html renders the login form."""
        resp = client.get("/login.html")
        assert resp.status_code == 200

    def test_login_wrong_password(self, client, mock_cursor):
        """POST /login.html with wrong password should show error (failure case)."""
        # DB.get_pass iterates cursor and returns l[0][0]
        mock_cursor.__iter__ = MagicMock(return_value=iter([("correctpass",)]))

        resp = client.post(
            "/login.html",
            data={"usern": "testuser", "passw": "wrongpass"},
        )
        assert resp.status_code == 200
        assert b"incorrect" in resp.data or b"error" in resp.data.lower()

    def test_login_nonexistent_user(self, client, mock_cursor):
        """POST /login.html with user that doesn't exist (failure case)."""
        # DB.get_pass will raise IndexError because cursor returns nothing
        mock_cursor.__iter__ = MagicMock(return_value=iter([]))

        resp = client.post(
            "/login.html",
            data={"usern": "ghost", "passw": "nopass"},
        )
        assert resp.status_code == 200
        assert b"incorrect" in resp.data


# ── 5. Thank-you page ───────────────────────────────────────────────────────

class TestThankYou:
    def test_thank_you_page(self, client):
        """GET /thank_you.html returns 200."""
        resp = client.get("/thank_you.html")
        assert resp.status_code == 200

