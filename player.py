import random
from typing import Tuple
import agents

Space = Tuple[int, int]

class OpenMoveEvalFn:
    def score(self, game, my_player=None):
        return len(game.getPlayerMoves(my_player)) - len(game.getOpponentMoves(my_player))


class Player:
    def __init__(self, search_depth=3, eval_fn=OpenMoveEvalFn()):

        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, time_left):
        best_move, _ = agents.alphabeta(
            self, game, time_left, depth=self.search_depth)
        return best_move

    def utility(self, game):
        return self.eval_fn.score(game, self)

class RandomPlayer:
    def __init__(self):
        pass

    def move(self, game, time_left):
        if not game.getPlayerMoves(self):
            return None
        return random.choice(game.getPlayerMoves(self))
