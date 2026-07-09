import pygame
from src.entities.tower import TOWER_TEMPLATES


class PlacementSystem:
    def __init__(self, grid):
        self.grid = grid
        self.selected_type = None
        self.ghost_pos = None
        self.ghost_valid = False

    def set_selected(self, tower_type):
        self.selected_type = tower_type

    def clear_selection(self):
        self.selected_type = None
        self.ghost_pos = None

    def update_ghost(self, mouse_pos, towers=None, camera=None):
        if not self.selected_type:
            self.ghost_pos = None
            return

        mx, my = mouse_pos
        if camera:
            mx += camera.x
            my += camera.y

        col, row = self.grid.pixel_to_tile(mx, my)
        px, py = self.grid.tile_to_pixel(col, row)

        self.ghost_pos = (px, py)
        self.ghost_valid = self._can_place(col, row, towers or [])

    def _tile_occupied(self, col, row, towers):
        for t in towers:
            tc, tr = self.grid.pixel_to_tile(t.x, t.y)
            if tc == col and tr == row:
                return True
        return False

    def _can_place(self, col, row, towers):
        if not (0 <= col < self.grid.cols and 0 <= row < self.grid.rows):
            return False
        if not self.grid.is_buildable(col, row):
            return False
        if self._tile_occupied(col, row, towers):
            return False
        return True

    def try_place(self, towers, cash):
        if not self.ghost_pos or not self.ghost_valid or not self.selected_type:
            return None, cash

        col, row = self.grid.pixel_to_tile(self.ghost_pos[0], self.ghost_pos[1])
        if self._tile_occupied(col, row, towers):
            return None, cash

        cost = TOWER_TEMPLATES[self.selected_type]["cost"]
        if cash < cost:
            return None, cash

        from src.entities.tower import Tower
        tower = Tower(self.ghost_pos[0], self.ghost_pos[1], self.selected_type,
                      grid_size=self.grid.tile_size)
        towers.append(tower)
        return tower, int(cash - cost)

    def render(self, surface, camera=None):
        if not self.ghost_pos or not self.selected_type:
            return

        px, py = self.ghost_pos
        if camera:
            px -= camera.x
            py -= camera.y

        ts = self.grid.tile_size
        if self.ghost_valid:
            ghost_surf = pygame.Surface((ts, ts), pygame.SRCALPHA)
            ghost_surf.fill((255, 255, 255, 60))
            pygame.draw.rect(ghost_surf, (255, 255, 255, 120), ghost_surf.get_rect(), 2)
            surface.blit(ghost_surf, (px, py))

            stats = TOWER_TEMPLATES[self.selected_type]
            if stats["range"] > 0:
                r = stats["range"]
                cx, cy = px + ts // 2, py + ts // 2
                range_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(range_surf, (255, 255, 255, 30), (r, r), r)
                pygame.draw.circle(range_surf, (255, 255, 255, 60), (r, r), r, 1)
                surface.blit(range_surf, (int(cx - r), int(cy - r)))
        else:
            ghost_surf = pygame.Surface((ts, ts), pygame.SRCALPHA)
            ghost_surf.fill((255, 0, 0, 60))
            pygame.draw.rect(ghost_surf, (255, 0, 0, 120), ghost_surf.get_rect(), 2)
            surface.blit(ghost_surf, (px, py))
