import unittest
from board import Board, State

class TestBoard(unittest.TestCase):
    def testFirstMoveOis(self):
        ois = 'O00AXT'
        game = Board(ois)
        should_be = [[State.BLANK] * game.width for _ in range(game.height)]
        should_be[0][0] = State.Q2

        self.assertEqual(game.state, should_be)
