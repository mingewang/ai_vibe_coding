import pygame


class HUD:
    def __init__(self, width=240):
        self.width = width
        self.bg_color = (30, 30, 40)
        self.text_color = (220, 220, 220)
        self.accent_color = (255, 200, 50)
        self.title_font = pygame.font.Font(None, 28)
        self.font = pygame.font.Font(None, 22)
        self.small_font = pygame.font.Font(None, 18)

    def render(self, surface, game_state):
        panel_rect = pygame.Rect(surface.get_width() - self.width, 0,
                                  self.width, surface.get_height())
        pygame.draw.rect(surface, self.bg_color, panel_rect)
        pygame.draw.line(surface, (60, 60, 80),
                         (panel_rect.left, 0), (panel_rect.left, surface.get_height()), 2)

        y = 10
        y = self._draw_section(surface, f"Wave {game_state['wave']}/{game_state['total_waves']}", y, self.title_font)
        y = self._draw_section(surface, f"{'IN PROGRESS' if game_state['wave_active'] else 'READY'}", y, self.small_font,
                               self.accent_color if game_state['wave_active'] else (100, 200, 100))
        y += 5

        y = self._draw_divider(surface, y)
        y = self._draw_section(surface, f"Cash: ${game_state['cash']}", y, self.font, self.accent_color)
        y = self._draw_section(surface, f"Lives: {game_state['lives']}", y, self.font,
                               (255, 80, 80) if game_state['lives'] <= 3 else self.text_color)
        y = self._draw_section(surface, f"Enemies: {game_state['enemies_alive']}", y, self.font)
        y += 5

        y = self._draw_divider(surface, y)
        y = self._draw_section(surface, "Towers", y, self.font)
        for tower_info in game_state.get('tower_counts', []):
            name, count, key = tower_info
            y = self._draw_section(surface, f"[{key}] {name}: {count}", y, self.small_font, (180, 180, 180))
        y += 5

        y = self._draw_divider(surface, y)
        y = self._draw_section(surface, "Controls", y, self.small_font, (150, 150, 150))
        controls = [
            "1-6: Select tower",
            "Click: Place tower",
            "RClick: Sell",
            "Space: Pause",
            "Enter: Start wave",
            "S: Stop spawning",
        ]
        for ctrl in controls:
            y = self._draw_section(surface, ctrl, y, self.small_font, (120, 120, 120))

        if game_state.get('game_over'):
            overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            go_font = pygame.font.Font(None, 64)
            go_text = go_font.render("GAME OVER", True, (255, 50, 50))
            text_rect = go_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(go_text, text_rect)
            restart_font = pygame.font.Font(None, 28)
            restart_text = restart_font.render("Press R to restart", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 50))
            surface.blit(restart_text, restart_rect)

        if game_state.get('all_waves_done') and not game_state.get('game_over'):
            overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            win_font = pygame.font.Font(None, 48)
            win_text = win_font.render("YOU WIN!", True, (50, 255, 50))
            text_rect = win_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(win_text, text_rect)

    def _draw_section(self, surface, text, y, font=None, color=None):
        if font is None:
            font = self.font
        if color is None:
            color = self.text_color
        label = font.render(text, True, color)
        surface.blit(label, (surface.get_width() - self.width + 10, y))
        return y + label.get_height() + 4

    def _draw_divider(self, surface, y):
        x = surface.get_width() - self.width
        pygame.draw.line(surface, (60, 60, 80), (x + 5, y), (surface.get_width() - 5, y), 1)
        return y + 8
