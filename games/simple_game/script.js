const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const overlay = document.getElementById('overlay');
const finalScoreEl = document.getElementById('finalScore');

const W = canvas.width, H = canvas.height;

let keys = {};
document.addEventListener('keydown', e => { keys[e.code] = true; if (e.code === 'Space') e.preventDefault(); });
document.addEventListener('keyup', e => { keys[e.code] = false; });

const player = { x: W/2, y: H - 60, speed: 4 };
let bullets = [];
let enemies = [];
let lastShot = 0, shotCooldown = 200;
let lastSpawn = 0, spawnInterval = 1000;
let score = 0;
let gameOver = false;

function spawnEnemy() {
  const x = 20 + Math.random() * (W - 40);
  const speed = 1.2 + Math.random() * 2.2;
  const size = 12 + Math.random() * 16;
  enemies.push({ x, y: -size, r: size, speed });
}

function endGame() {
  gameOver = true;
  overlay.classList.remove('hidden');
  finalScoreEl.textContent = 'Score: ' + score;
}

function restart() {
  bullets = [];
  enemies = [];
  score = 0;
  scoreEl.textContent = 'Score: 0';
  player.x = W/2; player.y = H - 60;
  spawnInterval = 1000;
  lastSpawn = Date.now();
  lastShot = 0;
  gameOver = false;
  overlay.classList.add('hidden');
}

function update(dt) {
  if (gameOver) return;
  if (keys['ArrowLeft']) player.x -= player.speed;
  if (keys['ArrowRight']) player.x += player.speed;
  if (keys['ArrowUp']) player.y -= player.speed;
  if (keys['ArrowDown']) player.y += player.speed;
  // clamp
  player.x = Math.max(12, Math.min(W-12, player.x));
  player.y = Math.max(12, Math.min(H-12, player.y));

  if (keys['Space'] && Date.now() - lastShot > shotCooldown) {
    bullets.push({ x: player.x, y: player.y - 18, vy: -7, r: 4 });
    lastShot = Date.now();
  }

  for (let i = bullets.length - 1; i >= 0; i--) {
    bullets[i].y += bullets[i].vy;
    if (bullets[i].y < -10) bullets.splice(i, 1);
  }

  if (Date.now() - lastSpawn > spawnInterval) {
    spawnEnemy();
    lastSpawn = Date.now();
    if (spawnInterval > 350) spawnInterval *= 0.99;
  }

  for (let i = enemies.length - 1; i >= 0; i--) {
    enemies[i].y += enemies[i].speed;
    if (enemies[i].y > H + 50) enemies.splice(i, 1);
  }

  // bullets vs enemies
  for (let i = enemies.length - 1; i >= 0; i--) {
    const e = enemies[i];
    for (let j = bullets.length - 1; j >= 0; j--) {
      const b = bullets[j];
      const dx = e.x - b.x, dy = e.y - b.y;
      if (dx*dx + dy*dy < (e.r + b.r) * (e.r + b.r)) {
        enemies.splice(i, 1);
        bullets.splice(j, 1);
        score += 10;
        scoreEl.textContent = 'Score: ' + score;
        break;
      }
    }
  }

  // enemies vs player
  for (let e of enemies) {
    const dx = e.x - player.x, dy = e.y - player.y;
    if (dx*dx + dy*dy < (e.r + 12) * (e.r + 12)) {
      endGame();
      break;
    }
  }
}

function drawPlayer() {
  ctx.save();
  ctx.translate(player.x, player.y);
  ctx.fillStyle = '#66d9ff';
  ctx.beginPath();
  ctx.moveTo(0, -14);
  ctx.lineTo(10, 12);
  ctx.lineTo(-10, 12);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function draw() {
  ctx.clearRect(0, 0, W, H);
  // stars background
  ctx.fillStyle = '#072';
  // bullets
  for (let b of bullets) {
    ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2); ctx.fillStyle = '#fff'; ctx.fill();
  }
  // enemies
  for (let e of enemies) {
    ctx.beginPath(); ctx.arc(e.x, e.y, e.r, 0, Math.PI*2); ctx.fillStyle = '#ff6b6b'; ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.08)'; ctx.stroke();
  }
  drawPlayer();
}

let lastTime = performance.now();
function loop(now) {
  const dt = now - lastTime;
  lastTime = now;
  update(dt);
  draw();
  requestAnimationFrame(loop);
}

requestAnimationFrame(loop);

// restart handler
document.addEventListener('keydown', e => {
  if (gameOver && e.code === 'KeyR') restart();
});
