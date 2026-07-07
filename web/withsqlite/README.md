# SQLite Blog MVP

A simple blog application built with Node.js, Express, and SQLite. It includes:

- user registration
- user login
- session-based authentication
- blog post creation for logged-in users only
- a home page that displays published posts

## Prerequisites

- Node.js 18+ recommended
- npm

## Getting started

1. Open the project directory:
   ```bash
   cd web/withsqlite
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the app:
   ```bash
   npm start
   ```

4. Open the app in your browser:
   ```text
   http://127.0.0.1:3100/
   ```

## Why use npm start instead of npm run dev?

This project uses a simple Node.js server entry point and does not define a custom development script such as `dev` in the package.json. The standard way to run it is:

```bash
npm start
```

If you want, the project can later be updated to support a `npm run dev` workflow with tools like `nodemon`.

## Running tests

```bash
npm test
```
