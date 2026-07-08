# Design

## Database Schema

```sql
CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT    UNIQUE NOT NULL,
    password    TEXT    NOT NULL,           -- hashed with passlib.hash.pbkdf2_sha256
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE posts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    body        TEXT    NOT NULL,
    author_id   INTEGER NOT NULL REFERENCES users(id),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

## Configuration (`config.py`)

| Key | Source | Default |
|---|---|---|
| `DATABASE` | `COMRITE_CLOUD_DATA_VOLUME` env + `blog.db` | `./data/blog.db` (relative to app dir) |
| `SECRET_KEY` | `SECRET_KEY` env | `dev-secret-key` |

## Routes

| Method | Path | Auth Required | Description |
|---|---|---|---|
| GET | `/` | No | List all posts |
| GET | `/post/<int:id>` | No | Show single post |
| GET | `/register` | No | Registration form |
| POST | `/register` | No | Create account |
| GET | `/login` | No | Login form |
| POST | `/login` | No | Authenticate |
| GET | `/logout` | Yes | Clear session |
| GET | `/create` | Yes | New post form |
| POST | `/create` | Yes | Save post |

## Auth Flow

- Passwords hashed with **pbkdf2_sha256** (via `passlib`).
- Session stored in signed Flask cookie; `user_id` stored in `session`.
- `@login_required` decorator checks `session.get("user_id")`; redirects to `/login` if missing.
- Logout clears `user_id` from session.

## Security Considerations (MVP)

- Passwords are hashed, never stored in plaintext.
- SQL queries use parameterized statements — no raw string interpolation.
- Session cookie is signed with Flask's `SECRET_KEY`.
- Basic input validation (non-empty fields, unique username).
- CSRF protection: not built-in for MVP (Flask-WTF optional later).
- XSS: Jinja2 auto-escapes HTML by default.

## Testing Strategy

- Use **pytest** + Flask test client.
- In-memory SQLite (`:memory:`) for test isolation.
- Test each route:
  - GET routes return 200.
  - POST routes with valid data redirect correctly.
  - POST routes with invalid data show errors / re-render form.
  - Authenticated-only routes redirect anonymous users to `/login`.
