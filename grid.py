import random
from tile import Tile, Cell

import math


class Vector:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Traversals:

    def __init__(self, x: list, y: list) -> None:
        self.x = x
        self.y = y


class Grid:

    def __init__(self, size: int):
        self.size = size
        self.start_tiles = 2

        self.cells = []

        self.build()
        self.player_turn = True

        # pre-allocate these objects (for speed)
        self.indexes = []
        for x in range(4):
            self.indexes.append([])
            for y in range(4):
                self.indexes[x].append(Cell(x, y))

        self.vectors = {
            0: Vector(0, -1)  # up
            ,
            1: Vector(1, 0)  # right
            ,
            2: Vector(0, 1)  # down
            ,
            3: Vector(-1, 0)  # left
        }

    # Build a grid of the specified size
    def build(self):
        for x in range(self.size):
            self.cells.append([])
            for y in range(self.size):
                self.cells[x].append(None)

    #print grid replace by to_string()
    # def print(self):
    #     for x in range(self.size):
    #         a_str = ""
    #         for y in range(self.size):
    #             a_str += str(self.cells[y][x]) + "\t"
    #         print(a_str)

    # Find the first available random position
    def random_available_cell(self) -> Cell:
        cells = self.available_cells()

        if len(cells) > 0:
            return cells[random.randrange(0, len(cells))]

    def available_cells(self) -> list:
        cells = []

        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y] is None:
                    cells.append(Cell(x, y))

        return cells

    # Check if there are any cells available
    def cells_available(self) -> bool:
        return len(self.available_cells()) > 0

    # Check if the specified cell is taken
    def cell_available(self, cell: Cell) -> bool:
        return not self.cell_occupied(cell)

    def cell_occupied(self, cell: Cell) -> bool:
        return not not self.cell_content(cell)

    def cell_content(self, cell: Cell) -> Tile:
        if self.within_bounds(cell):
            return self.cells[cell.x][cell.y]
        else:
            return None

    # Inserts a tile at its position
    def insert_tile(self, tile: Tile):
        self.cells[tile.x][tile.y] = tile

    def remove_tile(self, tile: Tile):
        self.cells[tile.x][tile.y] = None

    def within_bounds(self, position: Cell):
        return position.x >= 0 and position.x < self.size and position.y >= 0 and position.y < self.size

    def clone(self):
        new_grid = Grid(self.size)
        new_grid.player_turn = self.player_turn
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y] is not None:
                    new_grid.insert_tile(self.cells[x][y].clone())
        return new_grid

    # Set up the initial tiles to start the game with
    def add_start_tiles(self):
        for i in range(0, self.start_tiles):
            self.add_random_tile()

    # Adds a tile in a random position
    def add_random_tile(self):
        if self.cells_available():
            value = 2 if random.randrange(0, 10) < 9 else 4
            tile = Tile(self.random_available_cell(), value)
            self.insert_tile(tile)

    # Save all tile positions and remove merger info
    def prepare_tiles(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y] is not None:
                    self.cells[x][y].merged_from = None
                    self.cells[x][y].save_position()

    # Move a tile and its representation
    def move_tile(self, tile: Tile, cell: Cell):
        self.cells[tile.x][tile.y] = None
        self.cells[cell.x][cell.y] = tile
        tile.update_position(cell)

    def get_vector(self, direction: int):
        # Vectors representing tile movement
        return self.vectors[direction]

    # Move tiles on the grid in the specified direction
    # returns true if move was successful
    def move(self, direction: int):
        # 0: up, 1: right, 2:down, 3: left
        cell = None
        tile = None

        vector = self.get_vector(direction)
        traversals = self.build_traversals(vector)
        moved = False
        score = 0
        won = False

        # Save the current tile positions and remove merger information
        self.prepare_tiles()

        # Traverse the grid in the right direction and move tiles
        for x in traversals.x:
            for y in traversals.y:
                cell = self.indexes[x][y]
                tile = self.cell_content(cell)

                if tile is not None:
                    positions = self.find_farthest_position(cell, vector)
                    next = self.cell_content(positions["next"])

                    # Only one merger per row traversal?
                    if next is not None and next.value == tile.value and not next.merged_from:
                        merged = Tile(positions["next"], tile.value * 2)
                        merged.merged_from = [tile, next]

                        self.insert_tile(merged)
                        self.remove_tile(tile)

                        # Converge the two tiles' positions
                        tile.update_position(positions["next"])

                        # Update the score
                        score += merged.value

                        # The mighty 2048 tile
                        if merged.value == 2048:
                            won = True
                    else:
                        self.move_tile(tile, positions["farthest"])

                    if not self.positions_equal(cell, tile):
                        self.player_turn = False
                        moved = True  # The tile moved from its original cell!

        return {"moved": moved, "score": score, "won": won}

    def computer_move(self):
        self.add_random_tile()
        self.player_turn = True

    # Build a list of positions to traverse in the right order
    def build_traversals(self, vector) -> Traversals:
        traversals = Traversals([], [])

        for pos in range(self.size):
            traversals.x.append(pos)
            traversals.y.append(pos)

        # Always traverse from the farthest cell in the chosen direction
        if vector.x == 1:
            traversals.x.reverse()
        if vector.y == 1:
            traversals.y.reverse()

        return traversals

    def find_farthest_position(self, cell: Cell, vector: Vector) -> dict:
        # Progress towards the vector direction until an obstacle is found
        previous = cell
        cell = Cell(previous.x + vector.x, previous.y + vector.y)
        while self.within_bounds(cell) and self.cell_available(cell):
            previous = cell
            cell = Cell(previous.x + vector.x, previous.y + vector.y)
        return {
            "farthest": previous,
            "next": cell  # Used to check if a merge is required
        }

    def moves_available(self):
        return self.cells_available() or self.tile_matches_available()

    # Check for available matches between tiles (more expensive check)
    # returns the number of matches
    def tile_matches_available(self) -> bool:
        tile = None

        for x in range(self.size):
            for y in range(self.size):
                tile = self.cell_content(Cell(x, y))

                if tile is not None:
                    for direction in range(4):
                        vector = self.get_vector(direction)
                        cell = Cell(x + vector.x, y + vector.y)

                        other = self.cell_content(cell)

                        if other is not None and other.value == tile.value:
                            return True  # matches++; // These two tiles can be merged
        return False  # matches;

    def positions_equal(self, first: Cell, second: Cell):
        return first.x == second.x and first.y == second.y

    def to_string(self):
        string = ""
        for i in range(4):
            for j in range(4):
                if self.cells[j][i]:
                    string += str(self.cells[j][i].value) + "\t"
                else:
                    string += "_\t"
            string += "\n"
        return string

    # counts the number of isolated groups.
    def islands(self) -> int:

        def mark(x, y, value):
            if x >= 0 and x <= 3 and y >= 0 and y <= 3 and self.cells[x][
                    y] is not None and self.cells[x][
                        y].value == value and not self.cells[x][y].marked:
                self.cells[x][y].marked = True

                for direction in range(4):
                    vector = self.get_vector(direction)
                    mark(x + vector.x, y + vector.y, value)

        islands = 0

        for x in range(4):
            for y in range(4):
                if self.cells[x][y]:
                    self.cells[x][y].marked = False
        for x in range(4):
            for y in range(4):
                if self.cells[x][y] is not None and not self.cells[x][y].marked:
                    islands += 1
                    mark(x, y, self.cells[x][y].value)
        return islands

    #// measures how smooth the grid is (as if the values of the pieces
    #// were interpreted as elevations). Sums of the pairwise difference
    #// between neighboring tiles (in log space, so it represents the
    #// number of merges that need to happen before they can merge).
    #// Note that the pieces can be distant
    def smoothness(self) -> float:
        smoothness = 0.0
        for x in range(4):
            for y in range(4):
                if self.cell_occupied(self.indexes[x][y]):
                    value = math.log2(
                        self.cell_content(self.indexes[x][y]).value)
                    for direction in range(1, 3):
                        vector = self.get_vector(direction)
                        target_cell = self.find_farthest_position(
                            self.indexes[x][y], vector)["next"]

                        if self.cell_occupied(target_cell):
                            target = self.cell_content(target_cell)
                            target_value = math.log2(target.value)
                            smoothness -= abs(value - target_value)
        return smoothness

    # def monotonicity(self):
    #     marked = []
    #     queued = []
    #     highest_value = 0
    #     highest_cell = Cell(0, 0)
    #     for x in range(4):
    #         marked.append([])
    #         queued.append([])
    #         for y in range(4):
    #             marked[x].append(False)
    #             queued[x].append(False)
    #             if self.cells[x][y] is not None and self.cells[x][
    #                     y].value > highest_value:
    #                 highest_value = self.cells[x][y].value
    #                 highest_cell.x = x
    #                 highest_cell.y = y

    #     increases = 0
    #     cell_queue = [highest_cell]
    #     queued[highest_cell.x][highest_cell.y] = True
    #     mark_list = [highest_cell]
    #     mark_after = 1  # only mark after all queued moves are done, as if searching in parallel
    #     # todo ...

    # measures how monotonic the grid is. This means the values of the tiles are strictly increasing
    # or decreasing in both the left/right and up/down directions
    def monotonicity2(self):
        # scores for all four directions
        totals = [0, 0, 0, 0]

        # up/down direction
        for x in range(4):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and not self.cell_occupied(
                        self.indexes[x][next]):
                    next += 1
                if next >= 4:
                    next -= 1
                current_value = math.log2(
                    self.cell_content(
                        self.indexes[x][current]).value) if self.cell_occupied(
                            Cell(x, current)) else 0
                next_value = math.log2(
                    self.cell_content(
                        self.indexes[x][next]).value) if self.cell_occupied(
                            Cell(x, next)) else 0
                if current_value > next_value:
                    totals[0] += next_value - current_value
                elif next_value > current_value:
                    totals[1] += current_value - next_value
                current = next
                next += 1

        # left/right direction
        for y in range(4):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and not self.cell_occupied(
                        self.indexes[next][y]):
                    next += 1
                if next >= 4:
                    next -= 1
                current_value = math.log2(
                    self.cell_content(
                        self.indexes[current][y]).value) if self.cell_occupied(
                            Cell(current, y)) else 0
                next_value = math.log2(
                    self.cell_content(
                        self.indexes[next][y]).value) if self.cell_occupied(
                            Cell(next, y)) else 0
                if current_value > next_value:
                    totals[2] += next_value - current_value
                elif next_value > current_value:
                    totals[3] += current_value - next_value
                current = next
                next += 1
        return max(totals[0], totals[1]) + max(totals[2], totals[3])

    def max_value(self) -> float:
        max = 0
        for x in range(4):
            for y in range(4):
                if self.cell_occupied(self.indexes[x][y]):
                    value = self.cell_content(self.indexes[x][y]).value
                    if value > max:
                        max = value
        return math.log2(max)

    # check for win
    def is_win(self) -> bool:
        for x in range(4):
            for y in range(4):
                if self.cell_occupied(self.indexes[x][y]):
                    if self.cell_content(self.indexes[x][y]).value == 2048:
                        return True
        return False