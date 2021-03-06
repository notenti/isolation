def alphabeta(player, agents_turn: bool, game, depth: int, alpha: float = float("-inf"), beta=float("inf")):

    best_value = float("-inf")
    for move in game.getPlayerMoves(agents_turn):
        value = minValueAb(player,
                           agents_turn,
                           game.forecastMove(move)[0],
                           depth,
                           alpha=float("-inf"),
                           beta=float("inf"))

        if value == float("inf"):
            return move, value

        if value >= best_value:
            best_value, best_move = value, move

        alpha = max(alpha, best_value)
    return best_move, best_value


def maxValueAb(player, agents_turn: bool, game, depth: int, alpha: float, beta: float) -> float:
    """returns a utility value"""
    if depth == 1:
        return player.utility(game)

    val = float("-inf")
    for move in game.getPlayerMoves(agents_turn):
        val = max(val, minValueAb(player,
                                  agents_turn,
                                  game.forecastMove(move)[0],
                                  depth - 1,
                                  alpha,
                                  beta))
        if val >= beta:
            return val
        alpha = max(alpha, val)
    return val


def minValueAb(player, agents_turn: bool, game, depth: int, alpha: float, beta: float) -> float:
    """returns a utility value"""
    if depth == 1:
        return player.utility(game)

    val = float("inf")
    for move in game.getPlayerMoves(game.agentActive):
        val = min(val, maxValueAb(player,
                                  agents_turn,
                                  game.forecastMove(move)[0],
                                  depth - 1,
                                  alpha,
                                  beta))
        if val <= alpha:
            return val
        beta = min(beta, val)
    return val
