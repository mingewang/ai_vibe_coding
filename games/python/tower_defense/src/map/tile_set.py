import pygame
from src.map.grid import TILE_GRASS, TILE_ROAD, TILE_SPAWN, TILE_BASE


GRASS_COLOR = (60, 140, 60)
ROAD_COLOR = (140, 120, 100)
SPAWN_COLOR = (200, 50, 50)
BASE_COLOR = (50, 50, 180)
GRID_LINE_COLOR = (40, 100, 40)


class TileRenderer:
    def __init__(self, tile_size=32):
        self.tile_size = tile_size

    def render(self, surface, grid, camera=None):
        offset_x = camera.x if camera else 0
        offset_y = camera.y if camera else 0

        start_col = max(0, offset_x // self.tile_size)
        end_col = min(grid.cols, (offset_x + surface.get_width()) // self.tile_size + 1)
        start_row = max(0, offset_y // self.tile_size)
        end_row = min(grid.rows, (offset_y + surface.get_height()) // self.tile_size + 1)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                tile_type = grid.get_tile(col, row)
                px = col * self.tile_size - offset_x
                py = row * self.tile_size - offset_y

                if tile_type == TILE_GRASS:
                    color = GRASS_COLOR
                elif tile_type == TILE_ROAD:
                    color = ROAD_COLOR
                elif tile_type == TILE_SPAWN:
                    color = SPAWN_COLOR
                elif tile_type == TILE_BASE:
                    color = BASE_COLOR
                else:
                    color = GRASS_COLOR

                pygame.draw.rect(surface, color,
                                 (px, py, self.tile_size, self.tile_size))
                pygame.draw.rect(surface, GRID_LINE_COLOR,
                                 (px, py, self.tile_size, self.tile_size), 1)
