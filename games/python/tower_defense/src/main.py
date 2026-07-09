import sys
import math
import pygame

from src.core.game_loop import FixedTimestepLoop
from src.core.event_bus import EventBus, GameEvent
from src.core.camera import Camera
from src.entities.enemy import Enemy, ENEMY_TEMPLATES, SplitterEnemy
from src.entities.tower import Tower, TOWER_TEMPLATES
from src.entities.projectile import Projectile
from src.systems.pathfinding import a_star, path_to_waypoints
from src.systems.spatial_hash import SpatialHash
from src.systems.collision import resolve_projectile_enemy, get_enemies_in_radius
from src.systems.wave_spawner import WaveSpawner
from src.map.grid import create_default_map
from src.map.tile_set import TileRenderer
from src.ui.hud import HUD
from src.ui.tower_panel import TowerPanel
from src.ui.placement import PlacementSystem

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 640
GAME_AREA_WIDTH = 960
UI_WIDTH = SCREEN_WIDTH - GAME_AREA_WIDTH


class World:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.grid = create_default_map()
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.pending_splits = []

        self.spatial_hash = SpatialHash(cell_size=64)
        self.wave_spawner = WaveSpawner(self.grid.spawn_pos, event_bus)
        self.placement = PlacementSystem(self.grid)
        self.tower_panel = TowerPanel(GAME_AREA_WIDTH + 10, 300)

        self.cash = 300
        self.lives = 20
        self.game_over = False
        self.paused = False
        self.selected_tower = None
        self.show_range = False

        self._setup_event_handlers()
        self._assign_paths_to_enemies()

    def _setup_event_handlers(self):
        self.event_bus.subscribe(GameEvent.ENEMY_KILLED, self._on_enemy_killed)
        self.event_bus.subscribe(GameEvent.ENEMY_REACHED_END, self._on_enemy_reached_end)

    def _on_enemy_killed(self, **data):
        enemy = data.get("enemy")
        if enemy:
            self.cash += enemy.reward
            self.wave_spawner.on_enemy_killed()

    def _on_enemy_reached_end(self, **data):
        enemy = data.get("enemy")
        if enemy:
            self.lives -= enemy.damage
            self.wave_spawner.on_enemy_reached_end()
            if self.lives <= 0:
                self.lives = 0
                self.game_over = True

    def _assign_paths_to_enemies(self):
        for enemy in self.enemies:
            if enemy.active and not enemy.path:
                enemy.set_path(list(self.grid.path_waypoints))

    def reset(self):
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        self.pending_splits.clear()
        self.cash = 300
        self.lives = 20
        self.game_over = False
        self.paused = False
        self.selected_tower = None
        self.wave_spawner = WaveSpawner(self.grid.spawn_pos, self.event_bus)
        self._setup_event_handlers()

    def update(self, dt):
        if self.game_over or self.paused:
            return

        self.wave_spawner.update(dt, self.enemies)
        self._assign_paths_to_enemies()

        for enemy in self.enemies:
            if enemy.active:
                enemy.update(dt)
                if enemy.path_index >= len(enemy.path):
                    enemy.deactivate()
                    self.event_bus.emit(GameEvent.ENEMY_REACHED_END, enemy=enemy)

        for tower in self.towers:
            if tower.active:
                tower.update(dt, self.enemies, self.projectiles)
                if tower.tower_type == "cash_gen":
                    self.cash += tower.stats.get("cash_per_sec", 0) * dt

        for proj in self.projectiles:
            if proj.active:
                proj.update(dt)

        self._handle_collisions()
        self._handle_pending_splits()
        self._cleanup()
        self._rebuild_spatial_hash()

    def _handle_collisions(self):
        for proj in list(self.projectiles):
            if not proj.active:
                continue

            nearby = self.spatial_hash.get_nearby_pos(
                proj.x - proj.radius, proj.y - proj.radius,
                proj.radius * 2, proj.radius * 2
            )

            for entity in nearby:
                if not hasattr(entity, 'hp'):
                    continue
                result = resolve_projectile_enemy(proj, entity)
                if result == "splash":
                    splash_targets = get_enemies_in_radius(
                        proj.x, proj.y, proj.splash_radius, self.enemies
                    )
                    for splash_enemy in splash_targets:
                        if splash_enemy.active and id(splash_enemy) not in proj.hit_enemies:
                            splash_enemy.take_damage(proj.damage // 2)
                            proj.hit_enemies.add(id(splash_enemy))
                            self._check_split(splash_enemy)
                            if not splash_enemy.active:
                                self.event_bus.emit(GameEvent.ENEMY_KILLED, enemy=splash_enemy)
                    proj.active = False
                    break
                elif result:
                    self._check_split(entity)
                    if not entity.active:
                        self.event_bus.emit(GameEvent.ENEMY_KILLED, enemy=entity)
                    break

            if proj.active and not proj.hit_enemies and proj.chain_count > 0:
                self._handle_chain(proj)

    def _handle_chain(self, proj):
        candidates = [e for e in self.enemies if e.active and id(e) not in proj.hit_enemies]
        for _ in range(proj.chain_count):
            if not candidates:
                break
            closest = min(candidates, key=lambda e: math.hypot(proj.x - e.center_x, proj.y - e.center_y))
            if math.hypot(proj.x - closest.center_x, proj.y - closest.center_y) > 150:
                break
            closest.take_damage(proj.damage)
            proj.hit_enemies.add(id(closest))
            self._check_split(closest)
            if not closest.active:
                self.event_bus.emit(GameEvent.ENEMY_KILLED, enemy=closest)
            candidates.remove(closest)

    def _check_split(self, enemy):
        if not enemy.active and not getattr(enemy, '_split_handled', False):
            enemy._split_handled = True
            if getattr(enemy, 'enemy_type', None) == "splitter":
                scale = 0.6
                for _ in range(2):
                    split = SplitterEnemy(enemy.x + 10, enemy.y + 10, scale=scale)
                    if enemy.path:
                        split.set_path(list(enemy.path))
                        split.path_index = enemy.path_index
                    self.pending_splits.append(split)

    def _handle_pending_splits(self):
        if self.pending_splits:
            self.enemies.extend(self.pending_splits)
            self.pending_splits.clear()

    def _cleanup(self):
        self.enemies = [e for e in self.enemies if e.active]
        self.projectiles = [p for p in self.projectiles if p.active]

    def _rebuild_spatial_hash(self):
        self.spatial_hash.clear()
        for enemy in self.enemies:
            if enemy.active:
                self.spatial_hash.insert(enemy)

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
                return
            if event.key == pygame.K_RETURN:
                if not self.wave_spawner.wave_active and not self.wave_spawner.all_waves_done:
                    self.wave_spawner.start_next_wave()
                return

            tower_keys = {
                pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
                pygame.K_4: 3, pygame.K_5: 4, pygame.K_6: 5,
            }
            if event.key in tower_keys:
                idx = tower_keys[event.key]
                ttype = self.tower_panel.select_by_key(idx)
                self.placement.set_selected(ttype)
                return
            if event.key == pygame.K_s:
                self.wave_spawner.spawn_queue.clear()
                print("Spawn queue cleared")
                return
            if event.key == pygame.K_r:
                self.show_range = not self.show_range
                return

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if mx < GAME_AREA_WIDTH:
                self.placement.update_ghost(event.pos, self.towers)
            else:
                self.placement.ghost_pos = None
                self.tower_panel.update_hover(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if mx >= GAME_AREA_WIDTH:
                result = self.tower_panel.handle_click(event.pos)
                if result:
                    self.placement.set_selected(self.tower_panel.selected_type)
                return

            if event.button == 1:
                if self.placement.selected_type:
                    tower, new_cash = self.placement.try_place(self.towers, self.cash)
                    if tower:
                        self.cash = new_cash
                        self.event_bus.emit(GameEvent.TOWER_PLACED, tower=tower)
                        self._recheck_paths()
                else:
                    col, row = self.grid.pixel_to_tile(mx, my)
                    for tower in self.towers:
                        tc, tr = self.grid.pixel_to_tile(tower.x, tower.y)
                        if tc == col and tr == row:
                            self.selected_tower = tower
                            break

            elif event.button == 3:
                col, row = self.grid.pixel_to_tile(mx, my)
                found_tower = False
                for tower in list(self.towers):
                    tc, tr = self.grid.pixel_to_tile(tower.x, tower.y)
                    if tc == col and tr == row:
                        self.cash += tower.sell_value()
                        self.towers.remove(tower)
                        self.event_bus.emit(GameEvent.TOWER_SOLD, tower=tower)
                        self._recheck_paths()
                        if self.selected_tower == tower:
                            self.selected_tower = None
                        found_tower = True
                        break
                if not found_tower:
                    self.tower_panel.clear_selection()
                    self.placement.clear_selection()

    def _recheck_paths(self):
        walk_grid = self.grid.get_walkability_grid()
        start_tile = self.grid.pixel_to_tile(*self.grid.spawn_pos)
        end_tile = self.grid.pixel_to_tile(*self.grid.base_pos)

        new_path_tiles = a_star(start_tile, end_tile, walk_grid, self.grid.cols, self.grid.rows)
        if new_path_tiles:
            self.grid.set_path_waypoints(path_to_waypoints(new_path_tiles, self.grid.tile_size))
        else:
            new_waypoints = [
                self.grid.spawn_pos,
                self.grid.base_pos,
            ]
            self.grid.set_path_waypoints(new_waypoints)

    def get_state(self):
        tower_counts = {}
        for t in self.towers:
            name = t.stats["name"]
            tower_counts[name] = tower_counts.get(name, 0) + 1

        return {
            "wave": self.wave_spawner.wave_number,
            "total_waves": self.wave_spawner.total_waves,
            "wave_active": self.wave_spawner.wave_active,
            "cash": self.cash,
            "lives": self.lives,
            "enemies_alive": len(self.enemies),
            "tower_counts": [(k, v, ["1", "2", "3", "4", "5", "6"][i])
                             for i, (k, v) in enumerate(tower_counts.items())],
            "game_over": self.game_over,
            "all_waves_done": self.wave_spawner.all_waves_done,
            "paused": self.paused,
        }

    def get_selected_tower_info(self):
        if not self.selected_tower:
            return None
        t = self.selected_tower
        return {
            "name": t.stats["name"],
            "level": t.level,
            "damage": t.stats["damage"],
            "range": t.stats["range"],
            "fire_rate": t.stats["fire_rate"],
            "sell_value": t.sell_value(),
            "upgrade_cost": t.get_upgrade_cost(),
        }


class Renderer:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera
        self.tile_renderer = TileRenderer(tile_size=32)
        self.hud = HUD(width=UI_WIDTH)
        self.font = pygame.font.Font(None, 18)

    def render(self, world, alpha):
        self.screen.fill((20, 20, 30))

        game_surf = pygame.Surface((GAME_AREA_WIDTH, SCREEN_HEIGHT))
        game_surf.fill((40, 40, 50))

        self.tile_renderer.render(game_surf, world.grid, self.camera)

        for tower in world.towers:
            if tower.active:
                show_range = world.show_range or tower == world.selected_tower
                tower.draw(game_surf, self.camera, show_range=show_range)

        for enemy in world.enemies:
            if enemy.active:
                enemy.draw(game_surf, self.camera)

        for proj in world.projectiles:
            if proj.active:
                proj.draw(game_surf, self.camera)

        world.placement.render(game_surf, self.camera)

        self.screen.blit(game_surf, (0, 0))

        self.hud.render(self.screen, world.get_state())
        world.tower_panel.render(self.screen, world.cash)

        if world.selected_tower:
            info = world.get_selected_tower_info()
            if info:
                self._draw_tower_info(info)

        if world.paused and not world.game_over:
            pause_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pause_surf.fill((0, 0, 0, 120))
            self.screen.blit(pause_surf, (0, 0))
            p_font = pygame.font.Font(None, 48)
            p_text = p_font.render("PAUSED", True, (255, 255, 255))
            p_rect = p_text.get_rect(center=(GAME_AREA_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(p_text, p_rect)

    def _draw_tower_info(self, info):
        x, y = 10, SCREEN_HEIGHT - 130
        w, h = 300, 120
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 200))
        self.screen.blit(bg, (x, y))

        lines = [
            f"{info['name']} (Lv.{info['level']})",
            f"DMG: {info['damage']}  RNG: {info['range']}  ROF: {info['fire_rate']:.1f}/s",
            f"Sell: ${info['sell_value']}  Upgrade: ${info['upgrade_cost']}",
            "[U]pgrade  [R]ange toggle  Right-click to sell",
        ]
        for i, line in enumerate(lines):
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            text = self.font.render(line, True, color)
            self.screen.blit(text, (x + 10, y + 5 + i * 22))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense")
    clock = pygame.time.Clock()

    event_bus = EventBus()
    world = World(event_bus)
    camera = Camera(GAME_AREA_WIDTH, SCREEN_HEIGHT,
                    world.grid.width, world.grid.height)
    renderer = Renderer(screen, camera)

    loop = FixedTimestepLoop(target_fps=60)

    running = True
    quit_confirm = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_confirm = True

            elif event.type == pygame.KEYDOWN:
                if quit_confirm:
                    if event.key in (pygame.K_y, pygame.K_RETURN):
                        running = False
                    elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                        quit_confirm = False
                    continue

                if event.key == pygame.K_ESCAPE:
                    quit_confirm = True
                    continue

            world.handle_event(event)

        if not world.game_over and not world.paused and not quit_confirm:
            world.update(loop.target_dt)

        renderer.render(world, 1.0)

        if quit_confirm:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            q_font = pygame.font.Font(None, 36)
            q_text = q_font.render("Quit game?", True, (255, 255, 255))
            q_rect = q_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(q_text, q_rect)

            h_font = pygame.font.Font(None, 24)
            h_text = h_font.render("Y / Enter = Yes     N / Escape = No", True, (200, 200, 200))
            h_rect = h_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(h_text, h_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
