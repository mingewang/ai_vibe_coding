import math


TILE_GRASS = 0
TILE_ROAD = 1
TILE_SPAWN = 2
TILE_BASE = 3


class Grid:
    def __init__(self, cols, rows, tile_size=32):
        self.cols = cols
        self.rows = rows
        self.tile_size = tile_size
        self.width = cols * tile_size
        self.height = rows * tile_size
        self.tiles = [[TILE_GRASS for _ in range(cols)] for _ in range(rows)]
        self.spawn_pos = (0, 0)
        self.base_pos = (0, 0)
        self.path_waypoints = []

    def set_tile(self, col, row, tile_type):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.tiles[row][col] = tile_type

    def get_tile(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.tiles[row][col]
        return TILE_GRASS

    def is_walkable(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.tiles[row][col] in (TILE_ROAD, TILE_SPAWN, TILE_BASE)
        return False

    def is_buildable(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.tiles[row][col] == TILE_GRASS
        return False

    def pixel_to_tile(self, px, py):
        return (int(px // self.tile_size), int(py // self.tile_size))

    def tile_to_pixel(self, col, row):
        return (col * self.tile_size, row * self.tile_size)

    def tile_center(self, col, row):
        return (col * self.tile_size + self.tile_size // 2,
                row * self.tile_size + self.tile_size // 2)

    def get_walkability_grid(self):
        return [[self.is_walkable(c, r) for c in range(self.cols)] for r in range(self.rows)]

    def set_path_waypoints(self, waypoints):
        self.path_waypoints = waypoints


def create_default_map():
    grid = Grid(30, 20, tile_size=32)

    path_segments = [
        ((0, 7), (4, 7)),
        ((4, 4), (4, 7)),
        ((4, 4), (27, 4)),
        ((27, 4), (27, 7)),
        ((27, 7), (29, 7)),
    ]

    road_cells = set()
    for (c1, r1), (c2, r2) in path_segments:
        if c1 == c2:
            for r in range(min(r1, r2), max(r1, r2) + 1):
                road_cells.add((c1, r))
        else:
            for c in range(min(c1, c2), max(c1, c2) + 1):
                road_cells.add((c, r1))

    for col, row in road_cells:
        grid.set_tile(col, row, TILE_ROAD)

    grid.set_tile(0, 7, TILE_SPAWN)
    grid.set_tile(29, 7, TILE_BASE)

    grid.spawn_pos = grid.tile_center(0, 7)
    grid.base_pos = grid.tile_center(29, 7)

    waypoints = [
        (-grid.tile_size, grid.tile_center(0, 7)[1]),
        grid.tile_center(0, 7),
        grid.tile_center(4, 7),
        grid.tile_center(4, 4),
        grid.tile_center(27, 4),
        grid.tile_center(27, 7),
        grid.tile_center(29, 7),
        (grid.width + grid.tile_size, grid.tile_center(0, 7)[1]),
    ]
    grid.set_path_waypoints(waypoints)

    return grid
