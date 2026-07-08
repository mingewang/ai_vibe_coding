# Blog System

Minimal blog application built with **Flask + SQLite**.

Users can register, log in, and create posts. Only authenticated users can publish.

## Quick Start

```bash
# 1. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open http://127.0.0.1:5000
```

The SQLite database is stored in `./data/blog.db` by default.

## Environment Variables

| Variable | Purpose | Default |
|---|---|---|
| `COMRITE_CLOUD_DATA_VOLUME` | Persistent storage path (Comrite Cloud) | `./data/` |
| `SECRET_KEY` | Flask session signing key | `dev-secret-key-change-in-production` |

## Run Tests

```bash
pip install -r requirements.txt
pytest tests/
```

## Project Structure

```
web/python_sqlite/
├── app.py              # App factory & entry point
├── config.py           # Database path configuration
├── models.py           # SQLite schema + connection helpers
├── auth.py             # Register / login / logout routes
├── blog.py             # Post listing, viewing, creation routes
├── utils.py            # @login_required decorator
├── templates/          # Jinja2 templates
├── static/style.css    # Minimal styling
└── tests/test_app.py   # Integration tests
```
