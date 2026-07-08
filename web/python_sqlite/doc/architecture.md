# Architecture

## Overview

```
┌─────────────┐     ┌────────────────────┐     ┌──────────┐
│   Browser   │────▶│  Flask App (Python) │────▶│  SQLite  │
│ (Jinja HTML)│     │   (routes / auth /  │     │  .db file│
└─────────────┘     │    blog logic)      │     └──────────┘
                    └────────────────────┘
```

Flask serves HTML directly via Jinja2 templates. No REST API; no SPA.

## Directory Layout

```
web/python_sqlite/
├── app.py                 # Flask application entry point
├── config.py              # Configuration (DB path, secret key, etc.)
├── models.py              # SQLite schema & data-access functions
├── auth.py                # Registration / login / logout routes
├── blog.py                # Blog CRUD routes
├── templates/
│   ├── base.html          # Layout shell
│   ├── index.html         # Post listing
│   ├── login.html         # Login form
│   ├── register.html      # Register form
│   ├── create_post.html   # New post form
│   └── post.html          # Single post view
├── static/
│   └── style.css          # Minimal styling
├── proposal.md
├── architecture.md
├── design.md
├── README.md
└── tests/
    └── test_app.py        # Integration tests
```

## Data Flow

1. **Register** → POST `/register` → validate → insert user row → redirect to login
2. **Login** → POST `/login` → verify password → set `session[user_id]` → redirect to /
3. **Create Post** → GET `/create` (check session) → POST `/create` → insert post → redirect to /
4. **View Posts** → GET `/` → SELECT all posts (JOIN users for author name) → render index
5. **View Single Post** → GET `/post/<id>` → SELECT post → render detail

## Database Persistence

The SQLite `.db` file lives at `$COMRITE_CLOUD_DATA_VOLUME/blog.db` (default `/app/data/blog.db`) so data survives container restarts.
