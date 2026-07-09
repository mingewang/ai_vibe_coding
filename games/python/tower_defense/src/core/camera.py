import pygame


class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0
        self.y = 0

    def apply(self, rect_or_pos):
        if isinstance(rect_or_pos, pygame.Rect):
            return rect_or_pos.move(-self.x, -self.y)
        x, y = rect_or_pos
        return (x - self.x, y - self.y)

    def update(self, target_x=None, target_y=None):
        if target_x is not None:
            self.x = max(0, min(target_x - self.width // 2, self.world_width - self.width))
        if target_y is not None:
            self.y = max(0, min(target_y - self.height // 2, self.world_height - self.height))
