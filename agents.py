def alphabeta(player, game, time_left, depth, alpha=float("-inf"), beta=float("inf")):

    if time_left() < 1:
        raise Exception()

    best_value = float("-inf")

    for move in game.getPlayerMoves(player):

        value = min_value_ab(player, game.forecastMove(move)[0], 1, depth, time_left, alpha=float("-inf"), beta=float("inf"))

        if value == float("inf"):
            return move, value

        if value >= best_value:
            best_value, best_move = value, move

        alpha = max(alpha, best_value)

    return best_move, best_value

def max_value_ab(player, game, current_depth, desired_depth, time_left, alpha, beta):
    """returns a utility value"""
    if time_left() < 1:
        raise Exception()

    if current_depth == desired_depth:
        return player.utility(game)

    val = float("-inf")
    for move in game.getPlayerMoves(player):
        val = max(val, min_value_ab(player, game.forecastMove(move)[0],current_depth + 1, desired_depth, time_left, alpha, beta))
        if val >= beta:
            return val
        alpha = max(alpha, val)
    return val


def min_value_ab(player, game, current_depth, desired_depth, time_left, alpha, beta):
    """returns a utility value"""

    if time_left() < 1:
        print("AB - Timeout")
        raise Exception()

    if current_depth == desired_depth:
        return player.utility(game)

    val = float("inf")
    for move in game.getPlayerMoves(game.activePlayer):
        val = min(val, max_value_ab(player, game.forecastMove(move)[0],current_depth + 1, desired_depth, time_left, alpha, beta))
        if val <= alpha:
            return val
        beta = min(beta, val)
    return val