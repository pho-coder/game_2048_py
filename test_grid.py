import unittest
from grid import Grid

from tile import Cell, Tile


class TestGrid(unittest.TestCase):

    def setUp(self) -> None:
        self.grid = Grid(4)
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    @unittest.skip("skip")
    def test_init(self):
        print(self.grid.cells)

    @unittest.skip("skip")
    def test_insert_tile(self):
        tile1 = Tile(Cell(0, 0), 2)
        # tile2 = Tile(Position(0, 1), 4)
        self.grid.insert_tile(tile1)
        print(self.grid.cells)
        self.assertEqual(tile1, self.grid.cells[0][0])

    @unittest.skip("skip")
    def test_add_start_tiles(self):
        self.grid.add_start_tiles()
        self.grid.print()

    @unittest.skip("skip")
    def test_prepare_tiles(self):
        self.grid.add_start_tiles()
        self.grid.prepare_tiles()
        self.grid.print()

    @unittest.skip("skip")
    def test_move_tile(self):
        tile = Tile(Cell(0, 0), 2)
        self.grid.cells[0][0] = tile
        self.grid.move_tile(tile, Cell(0, 1))

    def test_find_farthest_position(self):
        tile1 = Tile(Cell(0, 0), 2)
        self.grid.cells[0][0] = tile1
        tile2 = Tile(Cell(0, 2), 2)
        self.grid.cells[0][2] = tile2
        a = self.grid.find_farthest_position(Cell(0, 0), self.grid.vectors[0])
        print(str(a["farthest"]))
        print(str(a["next"]))
        print(self.grid.to_string())

    def test_to_string(self):
        tile1 = Tile(Cell(0, 0), 2)
        self.grid.cells[0][0] = tile1
        tile2 = Tile(Cell(0, 2), 2)
        self.grid.cells[0][2] = tile2
        a = self.grid.find_farthest_position(Cell(0, 0), self.grid.vectors[0])
        print()
        print(self.grid.to_string())


if __name__ == '__main__':
    unittest.main()