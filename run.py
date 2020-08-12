from flask import Flask, render_template
from board import Board, Space
from player import AlphaBetaPlayer
from typing import Tuple
Space = Tuple[int, int]

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/move/<repres>')
def determineMove(repres: str) -> str:

    game = Board(repres)
    agent = AlphaBetaPlayer(game)
    move, _ = agent.move(depth=3)
    r, c = move
    return f'{r}{c}'

