import pygame


class Entity:
    __slots__ = ("x", "y", "width", "height", "active", "id")

    def __init__(self, x, y, width, height, eid=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = True
        self.id = eid

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def center(self):
        return (self.x + self.width / 2, self.y + self.height / 2)

    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    def distance_to(self, other):
        dx = self.center_x - other.center_x
        dy = self.center_y - other.center_y
        return (dx * dx + dy * dy) ** 0.5

    def deactivate(self):
        self.active = False
