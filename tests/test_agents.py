import unittest
from board import Board, State
from player import AlphaBetaPlayer, OpenMoveEvalFn


class TestAgents(unittest.TestCase):
    def testABOpenMoveEvaluation(self):
        ois = 'O33A25X01020405121520313234404252546062T'
        game = Board(ois)
        agent = AlphaBetaPlayer(game, eval_fn=OpenMoveEvalFn())

        expected_depth_scores = [(1, -2), (2, 1), (3, 4), (4, 3), (5, 5)]

        for depth, expected_score in expected_depth_scores:
            _, score = agent.move(depth)
            self.assertEqual(score, expected_score)




