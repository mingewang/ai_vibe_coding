import math
import pygame
from src.entities.base import Entity
from src.ai.state_machine import StateMachine
from src.ai.behaviors import FollowPath, Charge, Split, Regenerate


ENEMY_TEMPLATES = {
    "grunt": {
        "max_hp": 100, "speed": 1.0, "radius": 8, "color": (200, 50, 50),
        "reward": 10, "damage": 1, "behavior": "follow_path"
    },
    "charger": {
        "max_hp": 80, "speed": 2.5, "radius": 10, "color": (255, 100, 0),
        "reward": 20, "damage": 2, "behavior": "charge"
    },
    "flier": {
        "max_hp": 60, "speed": 1.4, "radius": 7, "color": (150, 200, 100),
        "reward": 15, "damage": 1, "behavior": "follow_path",
        "flying": True
    },
    "splitter": {
        "max_hp": 200, "speed": 0.8, "radius": 12, "color": (150, 50, 200),
        "reward": 30, "damage": 2, "behavior": "split"
    },
    "regenerator": {
        "max_hp": 150, "speed": 0.7, "radius": 9, "color": (0, 200, 100),
        "reward": 25, "damage": 1, "behavior": "regenerate",
        "regen_rate": 5, "regen_interval": 1.0
    },
    "boss": {
        "max_hp": 2000, "speed": 0.5, "radius": 20, "color": (200, 0, 0),
        "reward": 200, "damage": 5, "behavior": "follow_path"
    },
}


class Enemy(Entity):
    __slots__ = ("max_hp", "hp", "speed", "base_speed", "radius", "color",
                 "reward", "damage", "flying", "path", "path_index",
                 "distance_to_end", "state_machine", "slow_timer",
                 "_slow_multiplier", "enemy_type", "regen_rate",
                 "regen_interval", "_regen_timer", "_split_handled", "eid")

    _next_id = 0

    def __init__(self, x, y, enemy_type):
        tmpl = ENEMY_TEMPLATES[enemy_type]
        size = tmpl["radius"] * 2
        Enemy._next_id += 1
        super().__init__(x, y, size, size, eid=f"enemy_{Enemy._next_id}")
        self.max_hp = tmpl["max_hp"]
        self.hp = self.max_hp
        self.base_speed = tmpl["speed"]
        self.speed = tmpl["speed"]
        self.radius = tmpl["radius"]
        self.color = tmpl["color"]
        self.reward = tmpl["reward"]
        self.damage = tmpl["damage"]
        self.flying = tmpl.get("flying", False)
        self.path = []
        self.path_index = 0
        self.distance_to_end = float("inf")
        self.slow_timer = 0.0
        self._slow_multiplier = 1.0
        self.enemy_type = enemy_type
        self.regen_rate = tmpl.get("regen_rate", 0)
        self.regen_interval = tmpl.get("regen_interval", 0)
        self._regen_timer = 0.0

        self.state_machine = StateMachine(self)
        behavior = tmpl["behavior"]
        if behavior == "follow_path":
            self.state_machine.push_state(FollowPath())
        elif behavior == "charge":
            self.state_machine.push_state(Charge())
        elif behavior == "split":
            self.state_machine.push_state(Split())
        elif behavior == "regenerate":
            self.state_machine.push_state(Regenerate())

    def set_path(self, waypoints):
        self.path = waypoints
        self.path_index = 1 if len(waypoints) > 1 else 0
        if waypoints:
            self.x, self.y = waypoints[0]
            self._update_distance()

    def _update_distance(self):
        if self.path_index >= len(self.path):
            self.distance_to_end = 0
            return
        total = 0.0
        px, py = self.x, self.y
        for i in range(self.path_index, len(self.path)):
            nx, ny = self.path[i]
            total += math.hypot(nx - px, ny - py)
            px, ny = nx, ny
        self.distance_to_end = total

    def update(self, dt):
        if not self.active or not self.path:
            return

        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.slow_timer = 0
                self.speed = self.base_speed
        else:
            self.speed = self.base_speed

        if self.regen_rate > 0:
            self._regen_timer += dt
            if self._regen_timer >= self.regen_interval:
                self._regen_timer -= self.regen_interval
                self.hp = min(self.max_hp, self.hp + self.regen_rate)

        self.state_machine.update(dt)
        self._update_distance()

    def move_along_path(self, dt):
        if self.path_index >= len(self.path):
            return False

        sx, sy = self.x, self.y
        ex, ey = self.path[self.path_index]
        dx, dy = ex - sx, ey - sy
        dist = math.hypot(dx, dy)

        if dist == 0:
            self.path_index += 1
            return True

        step = self.speed * dt * 60
        if step >= dist:
            self.x, self.y = ex, ey
            self.path_index += 1
        else:
            ratio = step / dist
            self.x += dx * ratio
            self.y += dy * ratio

        return self.path_index < len(self.path)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.deactivate()
            return True
        return False

    def apply_slow(self, duration, multiplier=0.5):
        self.slow_timer = duration
        self._slow_multiplier = multiplier
        self.speed = self.base_speed * multiplier

    def draw(self, surface, camera=None):
        if not self.active:
            return
        cx, cy = self.center_x, self.center_y
        if camera:
            cx -= camera.x
            cy -= camera.y

        pygame.draw.circle(surface, self.color, (int(cx), int(cy)), self.radius)

        hp_ratio = self.hp / self.max_hp
        bar_w = self.radius * 2
        bar_h = 4
        bar_x = int(cx - bar_w / 2)
        bar_y = int(cy - self.radius - 8)
        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, (0, 255, 0) if hp_ratio > 0.3 else (255, 0, 0),
                         (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))

        if self.flying:
            pygame.draw.circle(surface, (255, 255, 255, 128),
                               (int(cx), int(cy)), self.radius + 2, 1)


class SplitterEnemy(Enemy):
    def __init__(self, x, y, scale=1.0):
        super().__init__(x, y, "splitter")
        if scale < 1.0:
            self.max_hp = int(self.max_hp * scale)
            self.hp = self.max_hp
            self.radius = int(self.radius * scale)
            self.width = self.height = self.radius * 2
            self.speed *= 1.2
