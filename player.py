import random
from typing import Callable, Tuple
import agents

Space = Tuple[int, int]

class OpenMoveEvalFn:
    def score(self, game, my_player=None):
        return len(game.getPlayerMoves(my_player)) - len(game.getOpponentMoves(my_player))


class Player:
    def __init__(self, search_depth: int = 3, eval_fn=OpenMoveEvalFn()):

        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, time_left: Callable[..., float]) -> Space:
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
        return random.choice(list(game.getPlayerMoves(self)))


class HumanPlayer:
    def move(self, game, time_left):
        legal_moves = game.getPlayerMoves(self)
        choice = {}

        if not legal_moves:
            print("No more moves left.")
            return None, None

        counter = 1
        for move in legal_moves:
            choice.update({counter: move})
            print('\t'.join(['[%d] (%d,%d)' % (counter, move[0], move[1])]))
            counter += 1

        valid_choice = False

        while not valid_choice:
            try:
                index = int(input('Select move index [1-' + str(len(legal_moves)) + ']:'))
                valid_choice = 1 <= index <= len(legal_moves)

                if not valid_choice:
                    print('Illegal move of queen! Try again.')
            except Exception:
                print('Invalid entry! Try again.')

        return choice[index]
