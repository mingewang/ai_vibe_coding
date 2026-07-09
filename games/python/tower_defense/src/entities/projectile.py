import math
import pygame


class Projectile:
    __slots__ = ("x", "y", "vx", "vy", "damage", "splash_radius", "pierce",
                 "slow_duration", "slow_multiplier", "chain_count", "lifetime",
                 "hit_enemies", "active", "radius")

    def __init__(self, x, y, vx, vy, damage, splash_radius=0, pierce=0,
                 slow_duration=0, slow_multiplier=0.5, chain_count=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.damage = damage
        self.splash_radius = splash_radius
        self.pierce = pierce
        self.slow_duration = slow_duration
        self.slow_multiplier = slow_multiplier
        self.chain_count = chain_count
        self.lifetime = 2.0
        self.hit_enemies = set()
        self.active = True
        self.radius = 4

    @property
    def center_x(self):
        return self.x

    @property
    def center_y(self):
        return self.y

    @property
    def center(self):
        return (self.x, self.y)

    def update(self, dt):
        if not self.active:
            return
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False

    def draw(self, surface, camera=None):
        if not self.active:
            return
        x, y = self.x, self.y
        if camera:
            x -= camera.x
            y -= camera.y

        if self.splash_radius > 0:
            pygame.draw.circle(surface, (60, 60, 60), (int(x), int(y)), self.radius + 1)
        elif self.pierce > 0:
            pygame.draw.circle(surface, (100, 150, 255), (int(x), int(y)), self.radius)
        elif self.slow_duration > 0:
            pygame.draw.circle(surface, (100, 200, 255), (int(x), int(y)), self.radius)
        else:
            pygame.draw.circle(surface, (255, 200, 50), (int(x), int(y)), self.radius)

    def distance_to(self, other):
        dx = self.x - other.center_x
        dy = self.y - other.center_y
        return math.hypot(dx, dy)
