import json
import os
from src.entities.enemy import ENEMY_TEMPLATES, Enemy


WAVE_DATA = {
    "waves": [
        {"enemies": [{"type": "grunt", "count": 10, "interval": 0.8}]},
        {"enemies": [{"type": "grunt", "count": 15, "interval": 0.6},
                     {"type": "charger", "count": 3, "interval": 1.5}]},
        {"enemies": [{"type": "flier", "count": 8, "interval": 1.0}]},
        {"enemies": [{"type": "splitter", "count": 4, "interval": 2.0}]},
        {"enemies": [{"type": "grunt", "count": 20, "interval": 0.4},
                     {"type": "regenerator", "count": 5, "interval": 1.2}]},
        {"enemies": [{"type": "charger", "count": 10, "interval": 1.0},
                     {"type": "flier", "count": 8, "interval": 0.8}]},
        {"enemies": [{"type": "splitter", "count": 6, "interval": 1.5},
                     {"type": "regenerator", "count": 6, "interval": 1.0}]},
        {"enemies": [{"type": "grunt", "count": 30, "interval": 0.3},
                     {"type": "charger", "count": 10, "interval": 0.8},
                     {"type": "boss", "count": 1, "interval": 0}]},
    ]
}


class WaveSpawner:
    def __init__(self, spawn_pos, event_bus=None):
        self.spawn_pos = spawn_pos
        self.event_bus = event_bus
        self.waves = list(WAVE_DATA["waves"])
        self.current_wave = -1
        self.spawn_queue = []
        self.spawn_timer = 0.0
        self.wave_active = False
        self.all_waves_done = False
        self._enemies_spawned_this_wave = 0
        self._total_enemies_this_wave = 0
        self._enemies_alive_this_wave = 0

    @property
    def wave_number(self):
        return self.current_wave + 1

    @property
    def total_waves(self):
        return len(self.waves)

    def start_next_wave(self):
        if self.current_wave + 1 >= len(self.waves):
            return False
        self.current_wave += 1
        wave = self.waves[self.current_wave]
        self.spawn_queue = []
        for entry in wave["enemies"]:
            for _ in range(entry["count"]):
                self.spawn_queue.append(entry["type"])
        import random
        random.shuffle(self.spawn_queue)
        self.spawn_timer = 0.0
        self.wave_active = True
        self._enemies_spawned_this_wave = 0
        self._total_enemies_this_wave = len(self.spawn_queue)
        self._enemies_alive_this_wave = 0
        if self.event_bus:
            from src.core.event_bus import GameEvent
            self.event_bus.emit(GameEvent.WAVE_STARTED, wave=self.wave_number)
        return True

    def update(self, dt, enemies):
        if not self.wave_active or not self.spawn_queue:
            return

        next_type = self.spawn_queue[0]
        tmpl = ENEMY_TEMPLATES[next_type]
        interval = 1.0

        for entry in self.waves[self.current_wave]["enemies"]:
            if entry["type"] == next_type:
                interval = entry["interval"]
                break

        self.spawn_timer += dt
        if self.spawn_timer >= interval:
            self.spawn_timer -= interval
            enemy_type = self.spawn_queue.pop(0)
            enemy = Enemy(self.spawn_pos[0], self.spawn_pos[1], enemy_type)
            enemies.append(enemy)
            self._enemies_spawned_this_wave += 1
            self._enemies_alive_this_wave += 1
            if self.event_bus:
                from src.core.event_bus import GameEvent
                self.event_bus.emit(GameEvent.ENEMY_SPAWNED, enemy=enemy)

    def on_enemy_killed(self):
        self._enemies_alive_this_wave -= 1
        self._check_wave_complete()

    def on_enemy_reached_end(self):
        self._enemies_alive_this_wave -= 1
        self._check_wave_complete()

    def _check_wave_complete(self):
        if self.wave_active and not self.spawn_queue and self._enemies_alive_this_wave <= 0:
            self.wave_active = False
            if self.event_bus:
                from src.core.event_bus import GameEvent
                self.event_bus.emit(GameEvent.WAVE_COMPLETED, wave=self.wave_number)
            if self.current_wave + 1 >= len(self.waves):
                self.all_waves_done = True
