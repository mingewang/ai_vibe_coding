import pgzrun
import math

TILE_SIZE = 40
COLS = 20
ROWS = 15
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE
PSPEED = 3
NSPEED = 1.5

FLOOR = (24, 24, 30)
FGRID = (34, 34, 42)
WALL = (50, 50, 62)
WTOP = (72, 72, 88)
PCOL = (70, 140, 255)
POUT = (40, 100, 210)
NCOL = (230, 75, 75)
NOUT = (190, 50, 50)
COIN = (255, 215, 0)
CIN = (255, 240, 160)
COUT = (200, 170, 0)
TX = (220, 220, 230)
TSH = (20, 20, 25)
WN = (80, 255, 110)

MAP_DATA = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1],
    [1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,2,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,3,0,0,0,0,0,0,0,0,3,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,1,0,2,0,0,0,0,0,0,0,1],
    [1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

walls = []
coins = []
npc_spawns = []
for row in range(ROWS):
    for col in range(COLS):
        t = MAP_DATA[row][col]
        x, y = col * TILE_SIZE, row * TILE_SIZE
        if t == 1:
            walls.append(Rect(x, y, TILE_SIZE, TILE_SIZE))
        elif t == 2:
            coins.append({
                'x': x + TILE_SIZE / 2, 'y': y + TILE_SIZE / 2,
                'collected': False, 'size': 10
            })
        elif t == 3:
            npc_spawns.append((col, row))
del row, col

TOTAL_COINS = len(coins)
score = 0
frame = 0

class Player:
    def __init__(self, col, row):
        self.x = col * TILE_SIZE + TILE_SIZE / 2
        self.y = row * TILE_SIZE + TILE_SIZE / 2
        self.size = 30

    @property
    def rect(self):
        s = self.size / 2
        return Rect(self.x - s, self.y - s, self.size, self.size)

    def update(self):
        dx, dy = 0, 0
        if keyboard.left or keyboard.a: dx = -1
        if keyboard.right or keyboard.d: dx = 1
        if keyboard.up or keyboard.w: dy = -1
        if keyboard.down or keyboard.s: dy = 1
        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        nx = self.x + dx * PSPEED
        r = Rect(nx - self.size/2, self.y - self.size/2, self.size, self.size)
        blocked = any(r.colliderect(w) for w in walls)
        blocked = blocked or any(r.colliderect(n.rect) for n in npcs)
        if not blocked:
            self.x = nx

        ny = self.y + dy * PSPEED
        r = Rect(self.x - self.size/2, ny - self.size/2, self.size, self.size)
        blocked = any(r.colliderect(w) for w in walls)
        blocked = blocked or any(r.colliderect(n.rect) for n in npcs)
        if not blocked:
            self.y = ny

    def draw(self):
        r = self.rect
        screen.draw.filled_rect(r, PCOL)
        screen.draw.rect(r, POUT)

class NPC:
    def __init__(self, col, row):
        self.x = col * TILE_SIZE + TILE_SIZE / 2
        self.y = row * TILE_SIZE + TILE_SIZE / 2
        self.size = 30
        self.dir = 1
        self.left = (col - 2) * TILE_SIZE + TILE_SIZE / 2
        self.right = (col + 2) * TILE_SIZE + TILE_SIZE / 2

    @property
    def rect(self):
        s = self.size / 2
        return Rect(self.x - s, self.y - s, self.size, self.size)

    def update(self):
        self.x += NSPEED * self.dir
        if self.x > self.right:
            self.x = self.right
            self.dir = -1
        elif self.x < self.left:
            self.x = self.left
            self.dir = 1

    def draw(self):
        r = self.rect
        screen.draw.filled_rect(r, NCOL)
        screen.draw.rect(r, NOUT)
        cx, cy = self.x, self.y - 8
        if self.dir > 0:
            screen.draw.line((cx - 5, cy - 4), (cx + 5, cy), NOUT)
            screen.draw.line((cx - 5, cy + 4), (cx + 5, cy), NOUT)
        else:
            screen.draw.line((cx + 5, cy - 4), (cx - 5, cy), NOUT)
            screen.draw.line((cx + 5, cy + 4), (cx - 5, cy), NOUT)

npcs = [NPC(c, r) for c, r in npc_spawns]
player = Player(10, 1)

def update():
    global score, frame
    frame += 1
    player.update()
    for n in npcs:
        n.update()
    pr = player.rect
    for c in coins:
        if not c['collected']:
            cr = Rect(c['x'] - c['size'], c['y'] - c['size'],
                      c['size'] * 2, c['size'] * 2)
            if pr.colliderect(cr):
                c['collected'] = True
                score += 1

def draw():
    screen.fill(FLOOR)

    for row in range(ROWS):
        for col in range(COLS):
            if MAP_DATA[row][col] != 1:
                screen.draw.rect(
                    Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), FGRID)

    for w in walls:
        screen.draw.filled_rect(w, WALL)
        screen.draw.filled_rect(Rect(w.x, w.y, w.w, 3), WTOP)
        screen.draw.filled_rect(Rect(w.x, w.y, 3, w.h), WTOP)

    for c in coins:
        if not c['collected']:
            bob = math.sin(frame * 0.06) * 2
            cy = c['y'] + bob
            screen.draw.filled_circle((c['x'], cy), c['size'], COUT)
            screen.draw.filled_circle((c['x'], cy), c['size'] - 2, COIN)
            screen.draw.filled_circle(
                (c['x'] - 3, cy - 3), c['size'] // 3, CIN)

    for n in npcs:
        n.draw()

    player.draw()

    txt = f"Coins: {score}/{TOTAL_COINS}"
    screen.draw.text(txt, (12, 12), color=TSH, fontsize=32)
    screen.draw.text(txt, (10, 10), color=TX, fontsize=32)

    if score == TOTAL_COINS:
        msg = "ALL COINS COLLECTED!"
        sw = len(msg) * 11
        screen.draw.text(msg, (WIDTH // 2 - sw // 2 + 2, HEIGHT // 2 + 2),
                         color=TSH, fontsize=40)
        screen.draw.text(msg, (WIDTH // 2 - sw // 2, HEIGHT // 2),
                         color=WN, fontsize=40)

pgzrun.go()
