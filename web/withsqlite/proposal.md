# Proposal: Simple SQLite Blog System

## 1. Objective
Build a lightweight blog application that uses SQLite as the database and supports:
- user registration
- user login
- blog post creation by authenticated users only
- viewing published posts

## 2. Goals
- Keep the project simple and easy to understand.
- Use SQLite for local persistence without requiring a separate database server.
- Provide a minimal but practical authentication flow.
- Allow only logged-in users to create or publish posts.

## 3. Scope
### In scope
- Register page
- Login page
- Home page showing blog posts
- Create post page
- SQLite schema for users and posts
- Session-based authentication

### Out of scope for MVP
- Rich text editor
- image uploads
- admin dashboard
- comments or likes
- password reset flow

## 4. User Stories
- As a visitor, I can register for an account.
- As a visitor, I can log in.
- As a logged-in user, I can create a new blog post.
- As a guest, I can view published posts.
- As a logged-in user, I can log out.

## 5. Suggested Tech Stack
- Node.js + Express
- SQLite3
- HTML/CSS/JavaScript
- Sessions or cookies for auth
- Password hashing with bcrypt

## 6. Success Criteria
- Users can register and log in successfully.
- Only authenticated users can access the post creation form.
- Posts are stored in SQLite and shown on the homepage.
- The app runs locally with a simple setup.

## 7. Review Notes
This proposal is intentionally simple and focused on a working MVP. If this direction looks good, the next step is to define the architecture and detailed implementation plan.
