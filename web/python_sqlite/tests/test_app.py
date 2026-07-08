import tempfile
import os
import pytest
from app import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    app = create_app(test_config={
        "DATABASE": db_path,
        "TESTING": True,
    })
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    """Register + login helper, returns a dict with id and username."""

    class AuthActions:
        def __init__(self, client):
            self._client = client

        def register(self, username="testuser", password="secret"):
            return self._client.post(
                "/register",
                data={"username": username, "password": password},
                follow_redirects=True,
            )

        def login(self, username="testuser", password="secret"):
            return self._client.post(
                "/login",
                data={"username": username, "password": password},
                follow_redirects=True,
            )

        def logout(self):
            return self._client.get("/logout", follow_redirects=True)

    return AuthActions(client)


class TestAuth:
    def test_register_page(self, client):
        resp = client.get("/register")
        assert resp.status_code == 200

    def test_register_success(self, auth):
        resp = auth.register()
        assert resp.status_code == 200
        assert b"Registration successful" in resp.data

    def test_register_duplicate_username(self, auth):
        auth.register()
        resp = auth.register()
        assert resp.status_code == 200
        assert b"Username already taken" in resp.data

    def test_register_empty_fields(self, client):
        resp = client.post(
            "/register", data={"username": "", "password": ""}, follow_redirects=True
        )
        assert resp.status_code == 200
        assert b"Username and password are required" in resp.data

    def test_login_page(self, client):
        resp = client.get("/login")
        assert resp.status_code == 200

    def test_login_success(self, auth):
        auth.register()
        resp = auth.login()
        assert resp.status_code == 200
        assert b"Logged in successfully" in resp.data

    def test_login_invalid(self, auth):
        resp = auth.login()  # no user registered yet
        assert resp.status_code == 200
        assert b"Invalid username or password" in resp.data

    def test_logout(self, auth):
        auth.register()
        auth.login()
        resp = auth.logout()
        assert resp.status_code == 200
        assert b"Logged out" in resp.data


class TestBlog:
    def test_index_empty(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"No posts yet" in resp.data

    def test_create_post_requires_login(self, client):
        resp = client.get("/create", follow_redirects=True)
        assert resp.status_code == 200
        assert b"Login" in resp.data

    def test_create_and_view_post(self, auth, client):
        auth.register()
        auth.login()

        resp = client.get("/create")
        assert resp.status_code == 200

        resp = client.post(
            "/create",
            data={"title": "Hello World", "body": "This is my first post."},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b"Post created" in resp.data
        assert b"Hello World" in resp.data

        resp = client.get("/")
        assert b"Hello World" in resp.data
        assert b"testuser" in resp.data

        resp = client.get("/post/1")
        assert resp.status_code == 200
        assert b"Hello World" in resp.data
        assert b"This is my first post" in resp.data

    def test_create_post_empty_fields(self, auth, client):
        auth.register()
        auth.login()
        resp = client.post(
            "/create", data={"title": "", "body": ""}, follow_redirects=True
        )
        assert resp.status_code == 200
        assert b"Title and body are required" in resp.data

    def test_view_nonexistent_post(self, client):
        resp = client.get("/post/999", follow_redirects=True)
        assert resp.status_code == 200
        assert b"Post not found" in resp.data
