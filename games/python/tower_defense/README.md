# Tower Defense

A desktop Tower Defense game in Python built with `pygame`. Demonstrates OOP, A\* pathfinding, spatial collision, enemy AI state machines, and a fixed-timestep game loop — concepts that are harder to pull off in browser-based games.

## Install

Requires Python 3.10+ and `pip`.

```bash
cd games/python/tower_defense
pip install -r requirements.txt
```

## Start

```bash
python -m src.main
```

## How to Play

**Goal:** Stop waves of enemies from reaching the end of the path. Earn cash by killing enemies, spend it on towers, and survive all 8 waves.

### Controls

| Key / Input | Action |
|-------------|--------|
| `1` – `6` | Select tower type (Arrow, Cannon, Sniper, Slow, Tesla, Cash Gen) |
| Left-click on map | Place selected tower (snaps to grid) |
| Right-click on tower | Sell it for 50% refund |
| Left-click on placed tower | Select it (shows info + range) |
| `U` | Upgrade selected tower |
| `R` | Toggle range overlay on all towers |
| `Enter` | Start next wave |
| `Space` | Pause / unpause |
| `Escape` | Quit |

### Towers

| # | Tower | Cost | Damage | Range | Special |
|---|-------|------|--------|-------|---------|
| 1 | Arrow | $50 | 15 | 120 | Cheap all-rounder |
| 2 | Cannon | $100 | 50 | 90 | AoE splash (radius 30) |
| 3 | Sniper | $150 | 100 | 300 | Pierces 1 extra enemy |
| 4 | Slow | $75 | 5 | 130 | Slows enemy 50% for 2s |
| 5 | Tesla | $200 | 25 | 110 | Chains to 3 nearby enemies |
| 6 | Cash Gen | $250 | — | — | Generates $5/s |

### Enemies

| Enemy | HP | Speed | Behavior |
|-------|-----|-------|----------|
| Grunt | 100 | 1.0 | Follows path |
| Charger | 80 | 2.5 | Charges (2× speed) when below 30% HP |
| Flier | 60 | 1.4 | Fast, ignores terrain (flying tag) |
| Splitter | 200 | 0.8 | Splits into 2 smaller copies on death |
| Regenerator | 150 | 0.7 | Heals 8 HP/s when below 50% HP |
| Boss | 2000 | 0.5 | Massive HP pool (wave 8) |

### Tips

- Build at **chokepoints** — corners where the path turns (tiles adjacent to the road).
- Lead enemy movement: place Sniper towers at the start of long straightaways.
- Drop a Slow tower near a Cannon for maximum splash coverage.
- Reinforce your defense between waves — you keep earned cash.
- If all path tiles are blocked, enemies fall back to a direct line — keep at least one lane open.
