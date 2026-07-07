const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const request = require('supertest');

const testDbPath = path.join(__dirname, '..', `test-routes-${Date.now()}.db`);
process.env.SQLITE_DB_PATH = testDbPath;

const app = require('../server');
const { initializeDatabase, closeDb } = require('../db');

test.before(async () => {
  await initializeDatabase();
});

test.after(async () => {
  await closeDb();
});

test('guest can view home page and registered user can create a post', async () => {
  const registerResponse = await request(app)
    .post('/register')
    .type('form')
    .send({ username: 'tester', email: 'tester@example.com', password: 'secret123' });

  assert.equal(registerResponse.status, 302);

  const agent = request.agent(app);
  const loginResponse = await agent
    .post('/login')
    .type('form')
    .send({ username: 'tester', password: 'secret123' });

  assert.equal(loginResponse.status, 302);

  const createPostResponse = await agent
    .post('/posts')
    .type('form')
    .send({ title: 'Regression Test Post', content: 'This post should persist.' });

  assert.equal(createPostResponse.status, 302);

  const homeResponse = await request(app).get('/');
  assert.equal(homeResponse.status, 200);
  assert.match(homeResponse.text, /Regression Test Post/);
});
