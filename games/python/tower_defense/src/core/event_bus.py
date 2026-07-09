from collections import defaultdict
from enum import Enum, auto


class GameEvent(Enum):
    ENEMY_SPAWNED = auto()
    ENEMY_KILLED = auto()
    ENEMY_REACHED_END = auto()
    TOWER_PLACED = auto()
    TOWER_UPGRADED = auto()
    TOWER_SOLD = auto()
    WAVE_STARTED = auto()
    WAVE_COMPLETED = auto()
    GAME_OVER = auto()
    CASH_CHANGED = auto()
    LIVES_CHANGED = auto()


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event: GameEvent, callback):
        self._subscribers[event].append(callback)

    def unsubscribe(self, event: GameEvent, callback):
        if callback in self._subscribers[event]:
            self._subscribers[event].remove(callback)

    def emit(self, event: GameEvent, **data):
        for callback in self._subscribers[event]:
            callback(**data)
