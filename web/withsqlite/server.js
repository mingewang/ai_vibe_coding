const path = require('path');
const express = require('express');
const session = require('express-session');
const {
  initializeDatabase,
  createUser,
  getUserByUsername,
  verifyPassword,
  createPost,
  getPosts,
} = require('./db');

const app = express();
const PORT = process.env.PORT || 3100;

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(
  session({
    secret: process.env.SESSION_SECRET || 'simple-blog-secret',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 24 * 60 * 60 * 1000 },
  })
);

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderLayout(title, body, req) {
  const isLoggedIn = Boolean(req.session.userId);
  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeHtml(title)}</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }
      nav { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
      form { display: flex; flex-direction: column; gap: 0.75rem; max-width: 400px; }
      input, textarea, button { padding: 0.7rem; font-size: 1rem; }
      .card { border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; border-radius: 8px; }
      .muted { color: #666; }
      .error { color: #b00020; }
      .success { color: #0a7d2e; }
    </style>
  </head>
  <body>
    <nav>
      <a href="/">Home</a>
      ${isLoggedIn ? '<a href="/posts/new">Create Post</a>' : '<a href="/login">Login</a>'}
      ${isLoggedIn ? '' : '<a href="/register">Register</a>'}
      ${isLoggedIn ? '<form action="/logout" method="post" style="display:inline"><button type="submit">Logout</button></form>' : ''}
    </nav>
    <h1>${escapeHtml(title)}</h1>
    ${body}
  </body>
</html>`;
}

function requireLogin(req, res, next) {
  if (!req.session.userId) {
    return res.redirect('/login');
  }
  next();
}

app.get('/', async (req, res) => {
  try {
    const posts = await getPosts();
    const postItems = posts.length
      ? posts.map((post) => `
        <div class="card">
          <h2>${escapeHtml(post.title)}</h2>
          <p class="muted">By ${escapeHtml(post.author_username)} on ${new Date(post.created_at).toLocaleString()}</p>
          <p>${escapeHtml(post.content)}</p>
        </div>`).join('')
      : '<p>No posts yet. Be the first to write one.</p>';

    const body = `
      <p>Welcome to the simple SQLite blog.</p>
      ${postItems}`;

    res.send(renderLayout('Blog Home', body, req));
  } catch (error) {
    console.error(error);
    res.status(500).send('Unable to load posts.');
  }
});

app.get('/register', (req, res) => {
  const body = `
    <form action="/register" method="post">
      <input name="username" placeholder="Username" required />
      <input name="email" type="email" placeholder="Email" required />
      <input name="password" type="password" placeholder="Password" required />
      <button type="submit">Register</button>
    </form>`;
  res.send(renderLayout('Register', body, req));
});

app.post('/register', async (req, res) => {
  const { username, email, password } = req.body;
  if (!username || !email || !password) {
    return res.status(400).send(renderLayout('Register', '<p class="error">All fields are required.</p>', req));
  }

  try {
    const userId = await createUser(username.trim(), email.trim(), password);
    req.session.userId = userId;
    req.session.username = username.trim();
    res.redirect('/');
  } catch (error) {
    console.error(error);
    res.status(400).send(renderLayout('Register', '<p class="error">Registration failed. Username or email may already be in use.</p>', req));
  }
});

app.get('/login', (req, res) => {
  const body = `
    <form action="/login" method="post">
      <input name="username" placeholder="Username" required />
      <input name="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>`;
  res.send(renderLayout('Login', body, req));
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    const user = await getUserByUsername(username.trim());
    if (!user) {
      return res.status(401).send(renderLayout('Login', '<p class="error">Invalid username or password.</p>', req));
    }

    const isValid = await verifyPassword(password, user.password_hash);
    if (!isValid) {
      return res.status(401).send(renderLayout('Login', '<p class="error">Invalid username or password.</p>', req));
    }

    req.session.userId = user.id;
    req.session.username = user.username;
    res.redirect('/');
  } catch (error) {
    console.error(error);
    res.status(500).send(renderLayout('Login', '<p class="error">Unable to log in.</p>', req));
  }
});

app.post('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/');
  });
});

app.get('/posts/new', requireLogin, (req, res) => {
  const body = `
    <form action="/posts" method="post">
      <input name="title" placeholder="Title" required />
      <textarea name="content" rows="8" placeholder="Write your post..." required></textarea>
      <button type="submit">Publish</button>
    </form>`;
  res.send(renderLayout('Create Post', body, req));
});

app.post('/posts', requireLogin, async (req, res) => {
  const { title, content } = req.body;
  if (!title || !content) {
    return res.status(400).send(renderLayout('Create Post', '<p class="error">Title and content are required.</p>', req));
  }

  try {
    await createPost(title.trim(), content.trim(), req.session.userId);
    res.redirect('/');
  } catch (error) {
    console.error(error);
    res.status(500).send(renderLayout('Create Post', '<p class="error">Unable to publish post.</p>', req));
  }
});

function startServer(port = PORT) {
  return initializeDatabase()
    .then(() => {
      return app.listen(port, '0.0.0.0', () => {
        console.log(`Blog app listening on http://0.0.0.0:${port}`);
      });
    })
    .catch((error) => {
      console.error('Failed to initialize database', error);
      process.exit(1);
    });
}

if (require.main === module) {
  startServer(PORT);
}

module.exports = app;
module.exports.startServer = startServer;
