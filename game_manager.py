from ai import AI
from grid import Grid


class GameManager:

    def __init__(self, size) -> None:
        self.size = size  # size of the grid

    def setup(self):
        self.grid = Grid(self.size)
        self.grid.add_start_tiles()
        print(self.grid.to_string())

        self.ai = AI(self.grid)

        self.times = 0
        self.score = 0
        self.over = False
        self.won = False

    # makes a given move and updates state
    def move(self, direction):
        result = self.grid.move(direction)
        self.times += 1
        self.score += result["score"]

        if not result["won"]:
            if result["moved"]:
                self.grid.computer_move()
        else:
            self.won = True

        if not self.grid.moves_available():
            self.over = True  # Game over!

    # moves continuously until game is over
    def run(self):
        best = self.ai.get_best()
        print("best: " + str(best["move"]))
        print(self.grid.to_string())
        self.move(best["move"])
        print("after move, times: " + str(self.times))
        print(self.grid.to_string())