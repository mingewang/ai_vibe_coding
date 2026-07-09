# Design

## Enemy Types & AI

| Enemy    | HP  | Speed | Behavior (FSM)                                           | Hard in Browser?                                       |
|----------|-----|-------|-----------------------------------------------------------|--------------------------------------------------------|
| Grunt    | 100 | 1.0   | `Idle → FollowPath → ReachEnd → Despawn`                  | Trivial baseline                                       |
| Charger  | 80  | 2.5   | `FollowPath → (HP<30% → Charge) → 2× speed, 0.5× damage` | Continuous speed modulation with HP threshold          |
| Flier    | 60  | 1.2   | `FollowPath → BypassTowers → ignore tower range`          | Requires separate collision layer + path height data   |
| Splitter | 200 | 0.8   | `FollowPath → (HP==0 → Split) → 2 smaller enemies`        | Dynamic entity injection mid-frame                     |
| Regenerator | 150 | 0.7 | `FollowPath → (HP<50% → Regen) → heal 5/s over 3s`       | Timed DOT/heal with state interruption                 |
| Boss     | 2000| 0.4   | `FollowPath → (phase 1) → (phase 2: summon minions)`      | Multi-phase state machine with sub-entity spawning     |

### FSM Implementation
- Each state has `enter()`, `update(dt)`, `exit()`.
- Transitions evaluated once per state tick; no hard-coded transition tables.
- Example:
  ```python
  class ChargeState(State):
      def enter(self, enemy):
          enemy.speed *= 2
          enemy.color = (255, 0, 0)
      def update(self, enemy, dt):
          enemy.move_along_path(dt * enemy.speed)
          if enemy.distance_to_end < 10:
              enemy.transition("follow_path")
  ```

## Tower Types & Targeting

| Tower     | Range | Damage | Fire Rate | Targeting Strategy                        | Special                         |
|-----------|-------|--------|-----------|-------------------------------------------|---------------------------------|
| Arrow     | 120   | 15     | 1.0/s     | `NearestToEnd` — closest enemy to goal    | Cheap, reliable                 |
| Cannon    | 90    | 50     | 0.5/s     | `HordeCenter` — center of dense cluster   | AoE splash (circle radius 30)   |
| Sniper    | 300   | 100    | 0.3/s     | `Weakest` — enemy with lowest current HP  | Pierces through 1 extra enemy   |
| Slow      | 130   | 5      | 2.0/s     | `Strongest` — enemy with highest max HP   | Applies slow (0.5× speed, 2s)   |
| Tesla     | 110   | 25     | 1.2/s     | `Nearest` — closest to tower              | Chain: hits 3 nearby enemies    |
| Cash_Gen  | —     | —      | —         | —                                         | Generates $5/s, no attack       |

### Targeting Strategies (Strategy Pattern)
```python
class TargetingStrategy(ABC):
    @abstractmethod
    def acquire(self, tower, enemies: list[Enemy]) -> Enemy | None:
        ...

class NearestToEnd(TargetingStrategy):
    def acquire(self, tower, enemies):
        return min(enemies, key=lambda e: e.distance_to_end)
```

## Collision System

### Broad Phase — Spatial Hash
- Grid cell size = 64px (2× projectile max radius).
- Entities hashed by `(x // cell_size, y // cell_size)`.
- Query: get entity's cell + 8 neighbors → candidate list.

### Narrow Phase — AABB & Circle
- Projectile vs Enemy: circle-circle intersection.
- Tower range vs Enemy: circle-point distance.
- AoE splash: circle contains many — distance check against blast center.

## Pathfinding — A\* Details

```
Heuristic: Octile distance (allows diagonal movement)
Grid: 2D bool array — walkable / blocked

function a_star(start, goal, grid):
    open = priority_queue((start, 0))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open not empty:
        current = open.pop()
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in grid.neighbors(current):
            tentative_g = g_score[current] + cost(current, neighbor)
            if tentative_g < g_score.get(neighbor, ∞):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                open.push(neighbor, f_score[neighbor])

    return []  # no path
```

- Cost includes penalty for being near towers (enemies avoid dense areas).
- Recalculation triggered only when tower placement blocks a tile on an active path.

## Map Design
```
Grid: 30 × 20 tiles (800×600 px at 40px tile)
Path: S-shaped from left edge to right edge
Tiles: grass (buildable), road (non-buildable), spawn, base
```

```
S . . . . . . . . . . . . . . . . . . . . . B . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . R R R R R R R R R R R R R R R R R R R R R R R . . .
. . . . R . . . . . . . . . . . . . . . . . . . . . R . . .
. . . . R . . . . . . . . . . . . . . . . . . . . . R . . .
R R R R R . . . . . . . . . . . . . . . . . . . . . R R R R
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
R R R R R . . . . . . . . . . . . . . . . . . . . . R R R R
. . . . R . . . . . . . . . . . . . . . . . . . . . R . . .
. . . . R . . . . . . . . . . . . . . . . . . . . . R . . .
. . . . R R R R R R R R R R R R R R R R R R R R R R R . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
```

`S` = spawn, `B` = base, `R` = road, `.` = grass

## Wave System
```json
{
  "waves": [
    { "enemies": [{"type": "grunt", "count": 10, "interval": 0.8}] },
    { "enemies": [{"type": "grunt", "count": 15, "interval": 0.6},
                   {"type": "charger", "count": 3, "interval": 1.5}] },
    { "enemies": [{"type": "flier", "count": 5, "interval": 1.0}] },
    { "enemies": [{"type": "splitter", "count": 4, "interval": 2.0}] },
    { "enemies": [{"type": "grunt", "count": 20, "interval": 0.4},
                   {"type": "regenerator", "count": 5, "interval": 1.2}] }
  ]
}
```

## UI / Controls
| Input              | Action                        |
|--------------------|-------------------------------|
| Left-click on tower icon | Select tower to place     |
| Left-click on map  | Place selected tower (snap to grid) |
| Right-click on placed tower | Sell tower (50% refund) |
| Space              | Toggle pause                  |
| 1-6                | Hotkey tower selection        |
| Scroll             | Camera pan (future)           |

## Rendering Order (painter's algorithm)
1. Ground tiles (grass/road)
2. Path overlay (dashed line for visual path)
3. Towers (with range circle on hover)
4. Enemies (with HP bar)
5. Projectiles
6. UI (HUD, panels, tooltips)
