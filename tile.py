class Cell:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + " " + str(self.y)


class Tile:

    def __init__(self,
                 position: Cell,
                 value: int,
                 previous_position=None,
                 merged_from=None):
        self.x = position.x
        self.y = position.y
        self.value = value if value else 2

        self.previous_position = previous_position
        self.merged_from = merged_from  # Tracks tiles that merged together

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.value == other.value

    def __str__(self):
        return str(self.value)
        # return "x: " + str(self.x) + " y: " + str(self.y) + " value: " + str(
        #     self.value)

    def save_position(self):
        self.previous_position = Cell(self.x, self.y)

    def update_position(self, position: Cell):
        self.x = position.x
        self.y = position.y

    def clone(self):
        new_tile = Tile(Cell(self.x, self.y), self.value)
        return new_tile
