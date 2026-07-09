# Tower Defense Game — Proposal

## Overview
A desktop Tower Defense game built in Python using `pygame`. This project demonstrates advanced programming concepts that are difficult to achieve in browser-based games: real-time pathfinding, spatial collision systems, polymorphic enemy state machines, and deterministic game loops with sub-stepping.

## Why Python (not a browser)?
| Concept | Browser Limitation | Python Advantage |
|---------|-------------------|------------------|
| Pathfinding | JS single-thread blocks UI on heavy A* runs | Offload A* to a thread or `multiprocessing` pool |
| Spatial collision | Canvas hit-testing is O(n²) for many entities | Quadtree / spatial hash + fixed-timestep sub-stepping |
| Enemy AI | Simple FSM in JS; hard to maintain | Full state machine (SMACH-like) with composable behaviors |
| Deterministic simulation | `requestAnimationFrame` timing is jittery | Fixed-timestep accumulator with alpha interpolation |
| Memory control | GC pauses | `__slots__`, object pools, manual resource mgmt |

## Core Features
1. **Grid-based map** with configurable paths (loaded from Tiled or JSON)
2. **A\* pathfinding** — dynamic recalculation when paths are blocked
3. **4+ enemy types** with distinct AI behaviors (charger, flier, splitter, regenerator)
4. **6+ tower types** with unique targeting strategies (nearest, weakest, area, sniper, slow, cash-generator)
5. **Spatial hash** collision for 100s of simultaneous projectiles
6. **Wave system** with scripted spawn patterns
7. **Economy** — earn cash per kill, spend on towers/upgrades
8. **UI** — drag-and-drop tower placement, upgrade panel, wave controls

## Non-Goals
- No multiplayer
- No WebGL / shaders (software-rendered for clarity)
- No persistence / save system (future scope)

## Milestones
1. **Phase 1** — Core engine: game loop, grid, pathfinding, entity base classes
2. **Phase 2** — Enemies & towers: 4 enemy types, 4 tower types, spatial hash combat
3. **Phase 3** — Waves & economy: wave scripting, cash, upgrades
4. **Phase 4** — Polish: UI, sound, balancing
