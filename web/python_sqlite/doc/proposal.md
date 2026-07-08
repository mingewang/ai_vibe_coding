# Blog System — Proposal

## Objective
Build a minimal, self-contained blog application where users can register, log in, and create posts. Only authenticated users are allowed to publish content.

## Tech Stack
- **Backend**: Python 3 + Flask
- **Database**: SQLite (single file, zero-config)
- **Auth**: Session-based (Flask sessions + bcrypt/passlib for password hashing)
- **Frontend**: Server-rendered HTML (Jinja2 templates) — no JS framework

## Scope (MVP)
| Feature | Description |
|---|---|
| User Registration | Create account with username + password |
| User Login / Logout | Session-based auth |
| Create Post | Authenticated user can write a title + body |
| List Posts | Public homepage showing all posts (title, author, timestamp) |
| View Post | Individual post detail page |

## Out of Scope (future)
- Comments
- Rich text editor / Markdown
- Pagination
- User roles (admin)
- Password reset
- API

## Deployment
Designed for Comrite Cloud: uses `COMRITE_CLOUD_DATA_VOLUME` env var to persist the SQLite database across restarts.
