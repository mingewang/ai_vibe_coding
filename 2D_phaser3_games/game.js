const config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 800 }, debug: false },
  },
  scene: { preload, create, update },
  backgroundColor: '#87CEEB',
};

let player, platforms, coins, scoreText, cursors, score = 0;

function preload() {
  createPlaceholderAssets.call(this);
}

function createPlaceholderAssets() {
  const g = this.make.graphics({ add: false });

  g.fillStyle(0xe74c3c);
  g.fillRect(0, 0, 32, 48);
  g.generateTexture('player', 32, 48);

  g.clear();
  g.fillStyle(0x4a752c);
  g.fillRect(0, 0, 64, 32);
  g.generateTexture('platform', 64, 32);

  g.clear();
  g.fillStyle(0x8B4513);
  g.fillRect(0, 0, 96, 32);
  g.generateTexture('ground', 96, 32);

  g.clear();
  g.fillStyle(0xffd700);
  g.fillCircle(10, 10, 10);
  g.generateTexture('coin', 20, 20);

  g.destroy();
}

function create() {
  platforms = this.physics.add.staticGroup();

  const ground = platforms.create(400, 584, 'ground');
  ground.setScale(8.34, 1).refreshBody();

  const plat1 = platforms.create(200, 450, 'platform');
  plat1.setScale(2, 1).refreshBody();
  const plat2 = platforms.create(600, 350, 'platform');
  plat2.setScale(2, 1).refreshBody();
  const plat3 = platforms.create(400, 220, 'platform');
  plat3.setScale(1.5, 1).refreshBody();

  player = this.physics.add.sprite(100, 500, 'player');
  player.setBounce(0.1);
  player.setCollideWorldBounds(true);

  this.physics.add.collider(player, platforms);

  coins = this.physics.add.staticGroup();
  spawnCoins.call(this);

  this.physics.add.overlap(player, coins, collectCoin, null, this);

  scoreText = this.add.text(16, 16, 'Score: 0', {
    fontSize: '24px',
    fill: '#fff',
    stroke: '#000',
    strokeThickness: 3,
  });

  cursors = this.input.keyboard.createCursorKeys();
}

function spawnCoins() {
  const coinPositions = [
    [200, 400], [250, 400],
    [600, 300], [650, 300],
    [400, 170], [440, 170], [360, 170],
    [80, 200], [720, 150],
  ];
  coinPositions.forEach(([x, y]) => {
    coins.create(x, y, 'coin');
  });
}

function collectCoin(_player, coin) {
  coin.destroy();
  score += 10;
  scoreText.setText('Score: ' + score);

  if (coins.countActive() === 0) {
    coins.clear(true, true);
    spawnCoins.call(this);
  }
}

function update() {
  if (cursors.left.isDown || this.input.keyboard.addKey('A').isDown) {
    player.setVelocityX(-250);
  } else if (cursors.right.isDown || this.input.keyboard.addKey('D').isDown) {
    player.setVelocityX(250);
  } else {
    player.setVelocityX(0);
  }

  if ((cursors.up.isDown || this.input.keyboard.addKey('W').isDown || this.input.keyboard.addKey('SPACE').isDown) && player.body.touching.down) {
    player.setVelocityY(-500);
  }
}

const game = new Phaser.Game(config);
