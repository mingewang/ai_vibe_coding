# Architecture

## High-Level Diagram

```
┌──────────────────────────────────────────────┐
│                  GameApp                      │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  │
│  │ GameLoop  │  │  Renderer  │  │  UIMgr   │  │
│  │(fixed-ts) │  │(pygame blit)│  │(menus)  │  │
│  └────┬─────┘  └────────────┘  └──────────┘  │
│       │                                        │
│  ┌────▼──────────────────────────────┐        │
│  │          World                    │        │
│  │  ┌──────────┐  ┌───────────────┐  │        │
│  │  │   Grid    │  │  SpatialHash  │  │        │
│  │  └──────────┘  └───────────────┘  │        │
│  │  ┌──────────┐  ┌───────────────┐  │        │
│  │  │ EnemyMgr  │  │  TowerMgr     │  │        │
│  │  └──────────┘  └───────────────┘  │        │
│  │  ┌──────────┐  ┌───────────────┐  │        │
│  │  │Projectile│  │  WaveCtrl     │  │        │
│  │  │  Mgr     │  │               │  │        │
│  │  └──────────┘  └───────────────┘  │        │
│  └────────────────────────────────────┘        │
└──────────────────────────────────────────────┘
```

## Module Map

```
src/
├── main.py              # Entry point
├── core/
│   ├── game_loop.py     # Fixed-timestep accumulator + interpolation
│   ├── event_bus.py     # Observer pattern for decoupled communication
│   └── camera.py        # Viewport scrolling / zoom
├── entities/
│   ├── base.py          # Entity ABC (pos, size, active flag)
│   ├── enemy.py         # Enemy base + FSM
│   ├── tower.py         # Tower base + targeting strategies
│   └── projectile.py    # Projectile with lifetime & pierce
├── systems/
│   ├── pathfinding.py   # A* with grid heuristics & jump-point opt
│   ├── spatial_hash.py  # 2D spatial hash for O(1) broad-phase
│   ├── collision.py     # Narrow-phase AABB / circle vs line
│   └── wave_spawner.py  # Timed spawn queues from wave data
├── ai/
│   ├── state_machine.py # Generic FSM with enter/update/exit
│   └── behaviors.py     # Enemy behaviors (charge, flee, split, regen)
├── map/
│   ├── grid.py          # Tile grid, walkability, path nodes
│   └── tile_set.py      # Tile rendering & animation
├── ui/
│   ├── hud.py           # Cash, lives, wave info
│   ├── tower_panel.py   # Buy / upgrade / sell panel
│   └── placement.py     # Ghost preview, snap-to-grid
└── data/
    └── waves.json       # Wave definitions
```

## Key Design Decisions

### 1. Fixed-Timestep Game Loop
- Logic runs at 60 Hz **fixed** timestep; rendering runs at display refresh.
- Accumulator pattern with alpha interpolation for smooth visuals.
- Deterministic simulation — same inputs → same outputs.

### 2. Entity-Component Lite (not full ECS)
- Base `Entity` class with `__slots__` for memory efficiency.
- Composition over inheritance: `Enemy` has-a `StateMachine`, `Tower` has-a `TargetStrategy`.
- Managers (`EnemyMgr`, `TowerMgr`) own pools of entities, iterate only active ones.

### 3. Spatial Hash for Collision
- Grid cell size = 2× max projectile radius.
- Insert entity on position change; query neighbor cells.
- O(1) lookup vs O(n²) brute force — critical for 100+ projectiles vs 50+ enemies.

### 4. Event Bus (Observer)
- Decouples systems: `EnemyKilled` → `Economy.add_cash()`, `WaveCtrl.check_completion()`.
- No direct imports between subsystems.

### 5. A\* with Blocking-Aware Recalculation
- Paths computed on wave start + whenever tower placement blocks current path.
- Cached per enemy until invalidated.
- Jump-point search optimization for open grids.

## Data Flow per Frame

```
Input → UIMgr.process()
     → World.update(dt):
         → WaveCtrl.spawn(dt)
         → EnemyMgr.update(dt)    # FSM tick, movement
         → TowerMgr.update(dt)    # Acquire target, fire
         → ProjectileMgr.update(dt) # Move + collision
         → CollisionSystem.resolve()
         → SpatialHash.rebuild()
     → Renderer.render(alpha)
```

## Threading Model
- Main thread: game loop, rendering, input.
- Worker thread: heavy A\* recalculations (enemy count > threshold).
- Synchronisation via `queue.Queue` — path results pushed back to main thread.
