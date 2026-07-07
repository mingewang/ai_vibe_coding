# Design: Simple SQLite Blog System

## 1. Purpose
This document describes the detailed design of a minimal blog system with SQLite-based storage and session-based authentication.

## 2. Core Features
### Registration
- User enters username, email, and password.
- Server validates the data.
- Password is hashed and saved in the users table.
- User is redirected to the login page or automatically logged in.

### Login
- User enters username/email and password.
- Server checks credentials against the users table.
- On success, a session is created and stored server-side or via signed cookie.
- User is redirected to the home page.

### Posting
- Only authenticated users can access the post form.
- The form includes title and content.
- Server saves the post with the current user id as author_id.
- The new post appears on the homepage.

## 3. UI Flow
1. Landing page shows latest posts.
2. Navigation includes:
   - Home
   - Register
   - Login
   - Create Post (visible only when logged in)
   - Logout

## 4. API / Route Design
- GET / : show homepage
- GET /register : show registration form
- POST /register : create new user
- GET /login : show login form
- POST /login : authenticate user
- POST /logout : destroy session
- GET /posts/new : show create-post form
- POST /posts : create a new post

## 5. Database Design Details
### users
- username: required, unique
- email: required, unique
- password_hash: required

### posts
- title: required
- content: required
- author_id: required
- created_at: auto-generated

## 6. Error Handling
- Duplicate username/email should show a clear message.
- Invalid login should return a friendly error.
- Missing fields should be rejected.
- Unauthorized access should redirect to login.

## 7. Implementation Notes
- Use SQLite with a single database file.
- Initialize tables on startup if they do not already exist.
- Keep the first version minimal and easy to test.
- Use simple templates or plain HTML responses for fast development.

## 8. Review Checklist
Please review the following before implementation:
- Is the scope appropriate for an MVP?
- Should the first version support markdown or plain text posts?
- Should posts be public immediately after creation?
- Should there be a basic user profile page later?
