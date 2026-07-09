from collections import defaultdict


class SpatialHash:
    def __init__(self, cell_size=64):
        self.cell_size = cell_size
        self.contents = defaultdict(set)

    def _hash_pos(self, x, y):
        return (int(x // self.cell_size), int(y // self.cell_size))

    def _get_cells_for_entity(self, entity):
        cells = set()
        cells.add(self._hash_pos(entity.x, entity.y))
        cells.add(self._hash_pos(entity.x + entity.width, entity.y))
        cells.add(self._hash_pos(entity.x, entity.y + entity.height))
        cells.add(self._hash_pos(entity.x + entity.width, entity.y + entity.height))
        return cells

    def insert(self, entity):
        for cell in self._get_cells_for_entity(entity):
            self.contents[cell].add(entity)

    def remove(self, entity):
        for cell in self._get_cells_for_entity(entity):
            self.contents[cell].discard(entity)

    def update(self, entity):
        for cell in list(self.contents.keys()):
            self.contents[cell].discard(entity)
            if not self.contents[cell]:
                del self.contents[cell]
        self.insert(entity)

    def get_nearby(self, entity):
        nearby = set()
        for cell in self._get_cells_for_entity(entity):
            nearby.update(self.contents.get(cell, set()))
        nearby.discard(entity)
        return nearby

    def get_nearby_pos(self, x, y, width=1, height=1):
        cells = set()
        cells.add(self._hash_pos(x, y))
        cells.add(self._hash_pos(x + width, y))
        cells.add(self._hash_pos(x, y + height))
        cells.add(self._hash_pos(x + width, y + height))
        nearby = set()
        for cell in cells:
            nearby.update(self.contents.get(cell, set()))
        return nearby

    def clear(self):
        self.contents.clear()
