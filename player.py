import random
from typing import Callable, Tuple
import agents

Space = Tuple[int, int]

class OpenMoveEvalFn:
    def score(self, game, agent_active=True):
        return len(game.getPlayerMoves(agent_active)) - len(game.getOpponentMoves(agent_active))


class AlphaBetaPlayer:
    def __init__(self, game, eval_fn=OpenMoveEvalFn()):

        self.eval_fn = eval_fn
        self.game = game

    def move(self, depth: int) -> Tuple[Space, float]:
        best_move, best_value = agents.alphabeta(self, True, self.game, depth=depth)
        return best_move, best_value

    def utility(self, game):
        return self.eval_fn.score(game)

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
