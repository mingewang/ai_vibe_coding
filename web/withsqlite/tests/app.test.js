const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');

const testDbPath = path.join(__dirname, '..', `test-app-${Date.now()}.db`);
process.env.SQLITE_DB_PATH = testDbPath;

const {
  initializeDatabase,
  createUser,
  getUserByUsername,
  createPost,
  getPosts,
  closeDb,
} = require('../db');

test('initializes tables and supports user/post lifecycle', async () => {
  await initializeDatabase();

  const userId = await createUser('alice', 'alice@example.com', 'secret123');
  assert.ok(userId > 0);

  const user = await getUserByUsername('alice');
  assert.equal(user.username, 'alice');
  assert.equal(user.email, 'alice@example.com');

  const postId = await createPost('Hello World', 'My first post', user.id);
  assert.ok(postId > 0);

  const posts = await getPosts();
  assert.equal(posts.length, 1);
  assert.equal(posts[0].title, 'Hello World');
  assert.equal(posts[0].author_username, 'alice');

  await closeDb();
});
