from typing import Callable


def alphabeta(player, game, time_left: Callable[..., float], depth: int, alpha: float = float("-inf"), beta=float("inf")):

    if time_left() < 1:
        raise Exception()

    best_value = float("-inf")

    for move in game.getPlayerMoves(player):

        value = minValueAb(player,
                           game.forecastMove(move)[0],
                           depth,
                           time_left,
                           alpha=float("-inf"),
                           beta=float("inf"))

        if value == float("inf"):
            return move, value

        if value >= best_value:
            best_value, best_move = value, move

        alpha = max(alpha, best_value)

    return best_move, best_value


def maxValueAb(player, game, depth: int, time_left: Callable[..., float], alpha: float, beta: float) -> float:
    """returns a utility value"""
    if time_left() < 1:
        raise Exception()

    if depth == 1:
        return player.utility(game)

    val = float("-inf")
    for move in game.getPlayerMoves(player):
        val = max(val, minValueAb(player,
                                  game.forecastMove(move)[0],
                                  depth - 1,
                                  time_left,
                                  alpha,
                                  beta))
        if val >= beta:
            return val
        alpha = max(alpha, val)
    return val


def minValueAb(player, game, depth: int, time_left: Callable[..., float], alpha: float, beta: float) -> float:
    """returns a utility value"""

    if time_left() < 1:
        print("AB - Timeout")
        raise Exception()

    if depth == 1:
        return player.utility(game)

    val = float("inf")
    for move in game.getPlayerMoves(game.activePlayer):
        val = min(val, maxValueAb(player,
                                  game.forecastMove(move)[0],
                                  depth - 1,
                                  time_left,
                                  alpha,
                                  beta))
        if val <= alpha:
            return val
        beta = min(beta, val)
    return val
