import random
from board import Board
from player import Player


Q1 = Player()
Q2 = Player()

game = Board(Q1, Q2)

for _ in range(2):
    moves = game.activeMoves
    random.shuffle(moves)
    game = game.forecastMove(moves[0])[0]

winner, history, termination = game.playIsolation(1000, print_moves=True)

print('\n', f'{winner} has won. Reason:  {termination}')