from src.ai.state_machine import State


class FollowPath(State):
    def update(self, enemy, dt):
        if not enemy.path or enemy.path_index >= len(enemy.path):
            return
        enemy.move_along_path(dt)


class Charge(State):
    def __init__(self):
        self._has_charged = False

    def enter(self, enemy):
        self._has_charged = False

    def update(self, enemy, dt):
        hp_ratio = enemy.hp / enemy.max_hp
        if hp_ratio < 0.3 and not self._has_charged:
            self._has_charged = True
            enemy.speed = enemy.base_speed * 2.0
            enemy.damage = enemy.damage // 2
            enemy.color = (255, 50, 0)

        if not enemy.path or enemy.path_index >= len(enemy.path):
            return
        enemy.move_along_path(dt)


class Split(State):
    def __init__(self):
        self._split_triggered = False

    def enter(self, enemy):
        self._split_triggered = False

    def update(self, enemy, dt):
        if not enemy.path or enemy.path_index >= len(enemy.path):
            return
        enemy.move_along_path(dt)


class Regenerate(State):
    def __init__(self):
        self._regen_active = False
        self._regen_timer = 0.0
        self._regen_duration = 3.0
        self._regen_rate = 8.0

    def enter(self, enemy):
        self._regen_active = False
        self._regen_timer = 0.0

    def update(self, enemy, dt):
        if not enemy.path or enemy.path_index >= len(enemy.path):
            return
        enemy.move_along_path(dt)

        hp_ratio = enemy.hp / enemy.max_hp
        if hp_ratio < 0.5 and not self._regen_active:
            self._regen_active = True
            self._regen_timer = 0.0
            enemy.color = (0, 255, 150)

        if self._regen_active:
            self._regen_timer += dt
            enemy.hp = min(enemy.max_hp, enemy.hp + self._regen_rate * dt)
            if self._regen_timer >= self._regen_duration:
                self._regen_active = False
                enemy.color = (0, 200, 100)
