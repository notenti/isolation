import random
from flask import Flask
from board import Board
from player import HumanPlayer, Player, RandomPlayer


app = Flask(__name__)

@app.route('/')
def play() -> str:
    Q1 = Player()
    Q2 = RandomPlayer()

    game = Board(Q1, Q2)

    for _ in range(2):
        moves = game.activeMoves
        # random.shuffle(moves)
        game = game.forecastMove(moves.pop())[0]

    winner, history, termination = game.playIsolation(1e6, print_moves=True)

    return f'{winner} has won. Reason:  {termination}'
