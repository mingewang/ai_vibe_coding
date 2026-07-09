import math
from abc import ABC, abstractmethod
import pygame
from src.entities.base import Entity
from src.entities.projectile import Projectile


TOWER_TEMPLATES = {
    "arrow": {
        "name": "Arrow", "cost": 50, "range": 120, "damage": 15,
        "fire_rate": 1.0, "color": (139, 90, 43), "projectile_speed": 400,
        "strategy": "nearest_to_end", "upgrade_cost": 40,
    },
    "cannon": {
        "name": "Cannon", "cost": 100, "range": 90, "damage": 50,
        "fire_rate": 0.5, "color": (80, 80, 80), "projectile_speed": 250,
        "strategy": "horde_center", "splash_radius": 30, "upgrade_cost": 75,
    },
    "sniper": {
        "name": "Sniper", "cost": 150, "range": 300, "damage": 100,
        "fire_rate": 0.3, "color": (50, 80, 120), "projectile_speed": 800,
        "strategy": "weakest", "pierce": 1, "upgrade_cost": 100,
    },
    "slow": {
        "name": "Slow", "cost": 75, "range": 130, "damage": 5,
        "fire_rate": 2.0, "color": (100, 180, 255), "projectile_speed": 300,
        "strategy": "strongest", "slow_duration": 2.0, "slow_multiplier": 0.5,
        "upgrade_cost": 50,
    },
    "tesla": {
        "name": "Tesla", "cost": 200, "range": 110, "damage": 25,
        "fire_rate": 1.2, "color": (200, 200, 50), "projectile_speed": 0,
        "strategy": "nearest", "chain_count": 3, "upgrade_cost": 150,
    },
    "cash_gen": {
        "name": "Cash Gen", "cost": 250, "range": 0, "damage": 0,
        "fire_rate": 0, "color": (255, 215, 0), "projectile_speed": 0,
        "strategy": "none", "cash_per_sec": 5, "upgrade_cost": 180,
    },
}


class TargetingStrategy(ABC):
    @abstractmethod
    def acquire(self, tower, enemies):
        ...


class NearestToEnd(TargetingStrategy):
    def acquire(self, tower, enemies):
        candidates = [e for e in enemies if e.active and tower.distance_to(e) <= tower.stats["range"]]
        if not candidates:
            return None
        return min(candidates, key=lambda e: e.distance_to_end)


class HordeCenter(TargetingStrategy):
    def acquire(self, tower, enemies):
        candidates = [e for e in enemies if e.active and tower.distance_to(e) <= tower.stats["range"]]
        if not candidates:
            return None
        avg_x = sum(e.center_x for e in candidates) / len(candidates)
        avg_y = sum(e.center_y for e in candidates) / len(candidates)
        return min(candidates, key=lambda e: math.hypot(e.center_x - avg_x, e.center_y - avg_y))


class Weakest(TargetingStrategy):
    def acquire(self, tower, enemies):
        candidates = [e for e in enemies if e.active and tower.distance_to(e) <= tower.stats["range"]]
        if not candidates:
            return None
        return min(candidates, key=lambda e: e.hp)


class Strongest(TargetingStrategy):
    def acquire(self, tower, enemies):
        candidates = [e for e in enemies if e.active and tower.distance_to(e) <= tower.stats["range"]]
        if not candidates:
            return None
        return max(candidates, key=lambda e: e.max_hp)


class Nearest(TargetingStrategy):
    def acquire(self, tower, enemies):
        candidates = [e for e in enemies if e.active and tower.distance_to(e) <= tower.stats["range"]]
        if not candidates:
            return None
        return min(candidates, key=lambda e: tower.distance_to(e))


STRATEGY_MAP = {
    "nearest_to_end": NearestToEnd(),
    "horde_center": HordeCenter(),
    "weakest": Weakest(),
    "strongest": Strongest(),
    "nearest": Nearest(),
}


class Tower(Entity):
    __slots__ = ("tower_type", "stats", "level", "fire_timer",
                 "targeting_strategy", "angle", "total_cost", "eid")

    _next_id = 0

    def __init__(self, x, y, tower_type, grid_size=32):
        Tower._next_id += 1
        super().__init__(x, y, grid_size, grid_size, eid=f"tower_{Tower._next_id}")
        self.tower_type = tower_type
        self.stats = dict(TOWER_TEMPLATES[tower_type])
        self.level = 1
        self.fire_timer = 0.0
        strat_key = self.stats.get("strategy", "nearest")
        self.targeting_strategy = STRATEGY_MAP.get(strat_key)
        self.angle = 0
        self.total_cost = self.stats["cost"]

    def update(self, dt, enemies, projectiles):
        if not self.active:
            return

        if self.tower_type == "cash_gen":
            return

        self.fire_timer -= dt
        if self.fire_timer <= 0:
            target = self.targeting_strategy.acquire(self, enemies) if self.targeting_strategy else None
            if target:
                self.fire_timer = 1.0 / self.stats["fire_rate"]
                self._fire(target, projectiles)

    def _fire(self, target, projectiles):
        sx, sy = self.center_x, self.center_y
        tx, ty = target.center_x, target.center_y
        dx, dy = tx - sx, ty - sy
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        self.angle = math.atan2(dy, dx)

        proj_speed = self.stats.get("projectile_speed", 300)
        proj = Projectile(
            sx, sy,
            dx / dist * proj_speed,
            dy / dist * proj_speed,
            self.stats["damage"],
            self.stats.get("splash_radius", 0),
            self.stats.get("pierce", 0),
            self.stats.get("slow_duration", 0),
            self.stats.get("slow_multiplier", 0.5),
            self.stats.get("chain_count", 0),
        )
        projectiles.append(proj)

    def get_upgrade_cost(self):
        return self.stats.get("upgrade_cost", 0) * self.level

    def upgrade(self):
        self.level += 1
        self.stats["damage"] = int(self.stats["damage"] * 1.3)
        self.stats["range"] = int(self.stats["range"] * 1.1)
        self.stats["fire_rate"] = min(self.stats["fire_rate"] * 1.15, 5.0)
        self.total_cost += self.get_upgrade_cost()

    def sell_value(self):
        return int(self.total_cost * 0.5)

    def draw(self, surface, camera=None, show_range=False):
        if not self.active:
            return
        x, y = self.x, self.y
        if camera:
            x -= camera.x
            y -= camera.y

        color = self.stats["color"]
        size = self.width - 4
        pygame.draw.rect(surface, color, (int(x + 2), int(y + 2), size, size))
        pygame.draw.rect(surface, (0, 0, 0), (int(x + 2), int(y + 2), size, size), 2)

        if self.level > 1:
            font = pygame.font.Font(None, 16)
            lvl_text = font.render(str(self.level), True, (255, 255, 255))
            surface.blit(lvl_text, (int(x + 4), int(y + 2)))

        ang = self.angle - math.pi / 2
        cx, cy = int(x + self.width / 2), int(y + self.height / 2)
        end_x = int(cx + math.cos(ang + math.pi / 2) * 12)
        end_y = int(cy + math.sin(ang + math.pi / 2) * 12)
        pygame.draw.line(surface, (0, 0, 0), (cx, cy), (end_x, end_y), 3)

        if show_range and self.stats["range"] > 0:
            r = self.stats["range"]
            range_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surf, (255, 255, 255, 40), (r, r), r)
            pygame.draw.circle(range_surf, (255, 255, 255, 80), (r, r), r, 1)
            surface.blit(range_surf, (int(cx - r), int(cy - r)))
