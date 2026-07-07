# Architecture: Simple SQLite Blog System

## 1. Overview
The application will follow a simple three-layer structure:
- Frontend: HTML pages and JavaScript for form handling
- Backend: Express server for routing and authentication
- Database: SQLite file storing users and posts

## 2. High-Level Components
### Client Layer
- Registration page
- Login page
- Home page for viewing posts
- Create post page

### Server Layer
- Auth routes: /register, /login, /logout
- Blog routes: /posts, /posts/new, /posts/create
- Middleware to protect post creation routes

### Data Layer
- SQLite database file, such as blog.db
- Tables:
  - users
  - posts

## 3. Request Flow
1. User opens the home page.
2. If not logged in, the user can register or log in.
3. After login, the server creates a session for the user.
4. When a logged-in user submits a new post, the server validates the session and saves the post.
5. The home page displays posts from the database.

## 4. Authentication Approach
- Store a hashed password in the users table.
- Create a session cookie after successful login.
- Protect create-post routes with authentication middleware.

## 5. Database Structure
### users
- id (INTEGER, primary key)
- username (TEXT, unique)
- email (TEXT, unique)
- password_hash (TEXT)
- created_at (TEXT)

### posts
- id (INTEGER, primary key)
- title (TEXT)
- content (TEXT)
- author_id (INTEGER, foreign key)
- created_at (TEXT)

## 6. Folder Structure
- public/ : HTML, CSS, JS assets
- routes/ : auth and blog route handlers
- db/ : SQLite initialization and connection
- server.js : entry point

## 7. Security Considerations
- Hash passwords before storing them.
- Use secure session cookies.
- Validate input on both client and server sides.
- Avoid exposing private routes to unauthenticated users.
