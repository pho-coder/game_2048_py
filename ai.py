import math
import time
from grid import Grid
import copy

from tile import Tile


class AI:

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def eval(self):
        empty_cells = len(self.grid.available_cells())
        smooth_weight = 0.1
        mono2_weight = 1.0
        empty_weight = 2.7
        max_weight = 1.0
        return self.grid.smoothness() * smooth_weight + self.grid.monotonicity2(
        ) * mono2_weight + math.log(
            empty_cells) * empty_weight + self.grid.max_value() * max_weight

    # alpha-beta depth first search
    def search(self, depth, alpha, beta, positions, cutoffs):
        best_score = None
        best_move = -1
        result = None

        # the maxing player
        if self.grid.player_turn:
            best_score = alpha
            for direction in range(4):
                new_grid = copy.deepcopy(self.grid)
                if new_grid.move(direction)["moved"]:
                    positions += 1
                    if new_grid.is_win():
                        return {
                            "move": direction,
                            "score": 10000,
                            "positions": positions,
                            "cutoffs": cutoffs
                        }
                    new_AI = AI(new_grid)

                    if depth == 0:
                        result = {"move": direction, "score": new_AI.eval()}
                    else:
                        result = new_AI.search(depth - 1, best_score, beta,
                                               positions, cutoffs)
                        if result["score"] > 9900:  # win
                            result[
                                "score"] -= 1  # to slightly penalize higher depth from win
                        positions = result["positions"]
                        cutoffs = result["cutoffs"]

                    if result["score"] > best_score:
                        best_score = result["score"]
                        best_move = direction
                    if best_score > beta:
                        cutoffs += 1
                        return {
                            "move": best_move,
                            "score": beta,
                            "positions": positions,
                            "cutoffs": cutoffs
                        }
        else:  # computer's turn, we'll do heavy pruning to keep the branching factor low
            best_score = beta

            # try a 2 and 4 in each cell and measure how annoying it is
            # with metrics from eval
            candidates = []
            cells = self.grid.available_cells()
            scores = {2: [], 4: []}
            for value in scores:
                for i in range(len(cells)):
                    scores[value].append(None)
                    cell = cells[i]
                    tile = Tile(cell, value)
                    self.grid.insert_tile(tile)
                    scores[value][
                        i] = -self.grid.smoothness() + self.grid.islands()
                    self.grid.remove_tile(cell)

            # now just pick out the most annoying moves
            max_score = max(max(scores[2]), max(scores[4]))
            for value in scores:  # 2 and 4
                for i in range(len(scores[value])):
                    if scores[value][i] == max_score:
                        candidates.append({
                            "position": cells[i],
                            "value": value
                        })

            # search on each candidate
            for i in range(len(candidates)):
                position = candidates[i]["position"]
                value = candidates[i]["value"]
                new_grid = copy.deepcopy(self.grid)
                tile = Tile(position, value)
                new_grid.insert_tile(tile)
                new_grid.player_turn = True
                positions += 1
                new_AI = AI(new_grid)
                result = new_AI.search(depth, alpha, best_score, positions,
                                       cutoffs)
                positions = result["positions"]
                cutoffs = result["cutoffs"]

                if result["score"] < best_score:
                    best_score = result["score"]
                if best_score < alpha:
                    cutoffs += 1
                    return {
                        "move": None,
                        "score": alpha,
                        "positions": positions,
                        "cutoffs": cutoffs
                    }
        return {
            "move": best_move,
            "score": best_score,
            "positions": positions,
            "cutoffs": cutoffs
        }

    # performs a search and returns the best move
    def get_best(self):
        return self.iterative_deep()

    # performs iterative deepening over the alpha-beta search
    def iterative_deep(self):
        start = time.time()
        depth = 0
        best = None
        while time.time() - start < 0.5:
            new_best = self.search(depth, -10000, 10000, 0, 0)
            if new_best["move"] == -1:
                break
            else:
                best = new_best
            depth += 1
        print("depth: " + str(depth))
        return best

    def translate(self, move):
        return {0: "up", 1: "right", 2: "down", 3: "left"}[move]
