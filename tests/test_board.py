import unittest
from board import Board, State

class TestBoard(unittest.TestCase):
    def testEmptyBoard(self):
        ois = 'OAXT'
        game = Board(ois)
        should_be = [[State.BLANK] * game.width for _ in range(game.height)]
        self.assertEqual(game.state, should_be)

    def testFirstMoveOis(self):
        ois = 'O00AXT'
        game = Board(ois)
        should_be = [[State.BLANK] * game.width for _ in range(game.height)]
        should_be[0][0] = State.Q2
        self.assertEqual(game.state, should_be)

    def testSecondMoveOis(self):
        ois = 'O00A01XT'
        game = Board(ois)
        should_be = [[State.BLANK] * game.width for _ in range(game.height)]
        should_be[0][0] = State.Q2
        should_be[0][1] = State.Q1
        self.assertEqual(game.state, should_be)

    def testComplexOisSansTrail(self):
        ois = 'O42A15X04061011121421222430323435404446545560T'
        game = Board(ois)
        board_state = [
            [" ", " ", " ", " ", "X", " ", "X"],
            ["X", "X", "X", " ", "X", "Q1", " "],
            [" ", "X", "X", " ", "X", " ", " "],
            ["X", " ", "X", " ", "X", "X", " "],
            ["X", " ", "Q2", " ", "X", " ", "X"],
            [" ", " ", " ", " ", "X", "X", " "],
            ["X", " ", " ", " ", " ", " ", " "]
        ]

        should_be = [[State(loc) for loc in row] for row in board_state]
        self.assertEqual(game.state, should_be)

    def testComplexOisWithTrail(self):
        ois = 'O42A15X04061011121421222430323435404446545560T1323334353'
        game = Board(ois)
        board_state = [
            [" ", " ", " ", " ", "X", " ", "X"],
            ["X", "X", "X", "O", "X", "Q1", " "],
            [" ", "X", "X", "O", "X", " ", " "],
            ["X", " ", "X", "O", "X", "X", " "],
            ["X", " ", "Q2", "O", "X", " ", "X"],
            [" ", " ", " ", "O", "X", "X", " "],
            ["X", " ", " ", " ", " ", " ", " "]
        ]

        should_be = [[State(loc) for loc in row] for row in board_state]
        self.assertEqual(game.state, should_be)

    def testComplexOisSansBlockWithTrail(self):
        ois = 'O42A06XT1323334353'
        game = Board(ois)
        board_state = [
            [" ", " ", " ", " ", " ", " ", "Q1"],
            [" ", " ", " ", "O", " ", " ", " "],
            [" ", " ", " ", "O", " ", " ", " "],
            [" ", " ", " ", "O", " ", " ", " "],
            [" ", " ", "Q2", "O", " ", " ", " "],
            [" ", " ", " ", "O", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "]
        ]

        should_be = [[State(loc) for loc in row] for row in board_state]
        self.assertEqual(game.state, should_be)
