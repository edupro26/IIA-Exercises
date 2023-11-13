"""
    Avaliação Contínua 3 - Kalah

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""


# ______________________________________________________________________________
# Evaluation function


def func_26(state, player):
    if state.is_game_over():
        result = state.result()
        return result * 100 if player == state.SOUTH else result * -100

    h1 = compareScores(state, player)
    h2 = comparePieces(state, player)
    h3 = possibleExtraMoves(state, player)
    h4 = possibleSteals(state, player)
    h5 = winningProbability(state, player)
    h6 = emptyPits(state, player)
    h7 = maxPlayerScore(state, player)
    h8 = minOpponentScore(state, player)

    total_pieces = state.NUM_PIECES
    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    if total_pieces - (south_score + north_score) < 10:
        weights = [1.12, 0.32, 0.68, 0.54, 0.62, 0.22, 0.66, 0.66]
    else:
        weights = [0.82, 0.08, 0.48, 0.34, 0.62, 0.04, 0.66, 0.66]
    value = sum(h * w for h, w in zip([h1, h2, h3, h4, h5, h6, h7, h8], weights))
    return value


# ______________________________________________________________________________
# Heuristics


def minOpponentScore(state, player):
    """ Attempts to minimize the opponent score """
    score = state.state[state.NORTH_SCORE_PIT] if player == state.SOUTH \
        else state.state[state.SOUTH_SCORE_PIT]
    return -score


def maxPlayerScore(state, player):
    """ Attempts to maximize the opponent score """
    score = state.state[state.SOUTH_SCORE_PIT] if player == state.SOUTH \
        else state.state[state.NORTH_SCORE_PIT]
    return score


def emptyPits(state, player):
    """ Compares the number of empty pits from the opponent
    side to the number of empty pits from the player side """
    playerEP, opponentEP = 0, 0
    for i in range(state.PLAY_PITS):
        player_pit = i if state.SOUTH else i + state.PLAY_PITS + 1
        opponent_pit = i + state.PLAY_PITS + 1 if player == state.SOUTH else i
        if state.state[player_pit] == 0:
            playerEP += 1
        if state.state[opponent_pit] == 0:
            opponentEP += 1
    return opponentEP - playerEP


def winningProbability(state, player):
    """ Evaluates the player's winning probability """
    value = 0
    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    if player == state.SOUTH and north_score >= 8:
        value += -((north_score * 1.5) - south_score)
    elif player == state.NORTH and south_score >= 8:
        value += -((south_score * 1.5) - north_score)
    return value


def possibleSteals(state, player):
    """ Counts possible pieces steals """
    count = 0
    for i in range(1, state.PLAY_PITS):
        player_pit = i if player == state.SOUTH \
            else i + state.PLAY_PITS + 1
        opponent_pit = 2 * state.PLAY_PITS - i if player == state.SOUTH \
            else state.PLAY_PITS - (i + 1)
        if state.state[player_pit] == 0 and state.state[opponent_pit] > 0:
            count += 1
    return count * 0.5


def possibleExtraMoves(state, player):
    """ Counts possible extra moves """
    count = 0
    score_pit = state.SOUTH_SCORE_PIT if player == state.SOUTH \
        else state.NORTH_SCORE_PIT
    for i in range(state.PLAY_PITS):
        pit = i if player == state.SOUTH else i + state.PLAY_PITS + 1
        if score_pit - pit == state.state[pit]:
            count += 1
    return count * 0.5


def comparePieces(state, player):
    """ Compares the pieces in the player side to
    the pieces in the opponent side """
    south_pieces, north_pieces = 0, 0
    for i in range(state.PLAY_PITS):
        south_pieces += state.state[i] * 0.25
        north_pieces += state.state[i + state.PLAY_PITS + 1] * 0.25
    return south_pieces - north_pieces if player == state.SOUTH \
        else north_pieces - south_pieces


def compareScores(state, player):
    """ Compares the player score with the opponent's """
    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    return south_score - north_score if player == state.SOUTH \
        else north_score - south_score