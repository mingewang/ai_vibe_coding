import math
import heapq


def heuristic(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)


def walkable_neighbors(pos, grid, cols, rows):
    x, y = pos
    dirs = [
        (1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
        (1, 1, math.sqrt(2)), (-1, 1, math.sqrt(2)),
        (1, -1, math.sqrt(2)), (-1, -1, math.sqrt(2)),
    ]
    for dx, dy, cost in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows:
            if not grid[ny][nx]:
                continue
            if dx != 0 and dy != 0:
                if not grid[y][nx] or not grid[ny][x]:
                    continue
            yield (nx, ny), cost


def a_star(start, goal, grid, cols, rows):
    if not (0 <= goal[0] < cols and 0 <= goal[1] < rows) or not grid[goal[1]][goal[0]]:
        return []
    if not (0 <= start[0] < cols and 0 <= start[1] < rows) or not grid[start[1]][start[0]]:
        return []

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0.0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor, move_cost in walkable_neighbors(current, grid, cols, rows):
            tentative_g = g_score[current] + move_cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                f_score[neighbor] = f
                heapq.heappush(open_set, (f, neighbor))

    return []


def path_to_waypoints(path, tile_size=32):
    if not path:
        return []
    waypoints = []
    for col, row in path:
        waypoints.append((col * tile_size + tile_size // 2, row * tile_size + tile_size // 2))
    return waypoints
