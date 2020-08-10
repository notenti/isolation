import random
from board import Board
from player import HumanPlayer, Player, RandomPlayer


Q1 = Player()
Q2 = RandomPlayer()

game = Board(Q1, Q2)

for _ in range(2):
    moves = game.activeMoves
    # random.shuffle(moves)
    game = game.forecastMove(moves.pop())[0]

winner, history, termination = game.playIsolation(1e6, print_moves=True)

print('\n', f'{winner} has won. Reason:  {termination}')