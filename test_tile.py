import unittest

from tile import Cell, Tile


class TestTile(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_save_position(self):
        position = Cell(1, 2)
        tile = Tile(position, 2)
        another_tile = Tile(position, 2, previous_position=position)
        self.assertEquals(tile, another_tile)

    def test_update_position(self):
        position = Cell(1, 2)
        tile = Tile(Cell(2, 3), 2)
        tile.update_position(position)
        self.assertEquals(tile.x, position.x)

    def test_clone(self):
        tile = Tile(Cell(1, 2), 2)
        new_tile = tile.clone()
        self.assertEquals(tile, new_tile)


if __name__ == '__main__':
    unittest.main()
