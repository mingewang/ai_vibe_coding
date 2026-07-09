import pygame
from src.entities.tower import TOWER_TEMPLATES


class TowerPanel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected_type = None
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
        self.tower_types = list(TOWER_TEMPLATES.keys())
        self.panel_width = 220
        self.item_height = 50
        self.padding = 5

        self.hovered_index = -1
        self.selected_index = -1

    def handle_click(self, mouse_pos):
        mx, my = mouse_pos
        for i, ttype in enumerate(self.tower_types):
            item_rect = pygame.Rect(
                self.x + self.padding,
                self.y + self.padding + i * (self.item_height + self.padding),
                self.panel_width - self.padding * 2,
                self.item_height
            )
            if item_rect.collidepoint(mx, my):
                if self.selected_type == ttype:
                    self.selected_type = None
                    self.selected_index = -1
                else:
                    self.selected_type = ttype
                    self.selected_index = i
                return ttype
        return None

    def update_hover(self, mouse_pos):
        mx, my = mouse_pos
        self.hovered_index = -1
        for i, ttype in enumerate(self.tower_types):
            item_rect = pygame.Rect(
                self.x + self.padding,
                self.y + self.padding + i * (self.item_height + self.padding),
                self.panel_width - self.padding * 2,
                self.item_height
            )
            if item_rect.collidepoint(mx, my):
                self.hovered_index = i
                break

    def select_by_key(self, key_index):
        if 0 <= key_index < len(self.tower_types):
            ttype = self.tower_types[key_index]
            if self.selected_type == ttype:
                self.selected_type = None
                self.selected_index = -1
            else:
                self.selected_type = ttype
                self.selected_index = key_index
            return self.selected_type
        return None

    def get_selected_tower(self):
        return self.selected_type

    def clear_selection(self):
        self.selected_type = None
        self.selected_index = -1

    def render(self, surface, cash):
        for i, ttype in enumerate(self.tower_types):
            stats = TOWER_TEMPLATES[ttype]
            item_rect = pygame.Rect(
                self.x + self.padding,
                self.y + self.padding + i * (self.item_height + self.padding),
                self.panel_width - self.padding * 2,
                self.item_height
            )

            bg_color = (50, 50, 60)
            if i == self.selected_index:
                bg_color = (60, 75, 100)
            elif i == self.hovered_index:
                bg_color = (65, 65, 80)
            pygame.draw.rect(surface, bg_color, item_rect)
            border_color = (180, 180, 220) if i == self.selected_index else (80, 80, 100)
            pygame.draw.rect(surface, border_color, item_rect, 2 if i == self.selected_index else 1)

            can_afford = cash >= stats["cost"]
            name_color = (255, 255, 255) if can_afford else (150, 150, 150)

            name_text = self.font.render(stats["name"], True, name_color)
            surface.blit(name_text, (item_rect.x + 5, item_rect.y + 3))

            cost_text = self.small_font.render(f"${stats['cost']}", True,
                                                (255, 200, 50) if can_afford else (150, 100, 50))
            surface.blit(cost_text, (item_rect.x + 5, item_rect.y + 22))

            dmg_text = self.small_font.render(f"DMG:{stats['damage']} RNG:{stats['range']}", True, (180, 180, 180))
            surface.blit(dmg_text, (item_rect.x + 80, item_rect.y + 22))

            color_preview = stats["color"]
            pygame.draw.rect(surface, color_preview,
                             (item_rect.right - 25, item_rect.y + 10, 16, 16))
            pygame.draw.rect(surface, (0, 0, 0),
                             (item_rect.right - 25, item_rect.y + 10, 16, 16), 1)
