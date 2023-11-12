"""
    Avaliação Contínua 3

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""

from tournament import *


# ______________________________________________________________________________
# Evaluation functions

# https://digitalcommons.andrews.edu/cgi/viewcontent.cgi?article=1259&context=honors

def func_26_v4(state, player):
    if state.is_game_over():
        result = state.result()
        return result * 100 if player == state.SOUTH else result * -100

    h1 = compareScores(state, player)
    h2 = comparePieces(state, player)
    h3 = possibleExtraMoves(state, player)
    h4 = possibleSteals(state, player)
    h5 = winningProbability(state, player)
    h6 = opponentEmptyPits(state, player)

    total_pieces = state.NUM_PIECES
    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    if total_pieces - (south_score + north_score) < 10:
        weights = [0.8, 0.5, 0.8, 0.4, 0.3, 0.4]  # More tunnig needed
    else:
        weights = [0.8, 0.1, 0.4, 0.2, 0.6, 0.2]  # More tunnig needed
    value = sum(h * w for h, w in zip([h1, h2, h3, h4, h5, h6], weights))
    return value


def opponentEmptyPits(state, player):
    count = 0
    for i in range(state.PLAY_PITS):
        pit = i if player == state.NORTH else i + state.PLAY_PITS + 1
        if state.state[pit] == 0:
            count += 1
    return count


def winningProbability(state, player):
    value = 0
    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    if player == state.SOUTH and north_score >= 8:
        value += -((north_score * 1.5) - south_score)
    elif player == state.NORTH and south_score >= 8:
        value += -((south_score * 1.5) - north_score)
    return value


def possibleSteals(state, player):
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
    count = 0
    score_pit = state.SOUTH_SCORE_PIT if player == state.SOUTH \
        else state.NORTH_SCORE_PIT
    for i in range(state.PLAY_PITS):
        pit = i if player == state.SOUTH else i + state.PLAY_PITS + 1
        if score_pit - pit == state.state[pit]:
            count += 1
    return count * 0.5


def comparePieces(state, player):
    south_pieces, north_pieces = 0, 0
    for i in range(state.PLAY_PITS):
        south_pieces += state.state[i] * 0.25
        north_pieces += state.state[i + state.PLAY_PITS + 1] * 0.25
    return south_pieces - north_pieces if player == state.SOUTH \
        else north_pieces - south_pieces


def compareScores(state, player):
    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    return south_score - north_score if player == state.SOUTH \
        else north_score - south_score


def func_26_v3(state, player):
    value = 0
    if state.is_game_over():
        result = state.result()
        return result*100 if player == state.SOUTH else result*-100

    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    if player == state.SOUTH:
        score_pit = state.SOUTH_SCORE_PIT
        for i in range(state.PLAY_PITS):
            if score_pit - i == state.state[i]:
                value += 1
        value += (south_score - north_score)
    else:
        score_pit = state.NORTH_SCORE_PIT
        for i in range(state.PLAY_PITS):
            if score_pit - (i+7) == state.state[i+7]:
                value += 1
        value += (north_score - south_score)

    return value


# ______________________________________________________________________________
# TESTS

aleatorio = JogadorAleat("Aleatório")
el_caos_int = JogadorAlfaBeta("El Caos Inteligente", 3, f_caos_intel)
chapiteau = JogadorAlfaBeta("Chapiteau", 3, chapiteau_replica)
jogador_26_v3 = JogadorAlfaBeta("Jogador26_v3", 3, func_26_v3)
jogador_26_v4 = JogadorAlfaBeta("Jogador26_v4", 3, func_26_v4)

win_rates = []
player1, player2 = 0, 0
for i in range(7):
    res = torneio(50, [jogador_26_v3, jogador_26_v4], 10)
    print(res)
    player1 += res["Jogador26_v3"]
    player2 += res["Jogador26_v4"]
    win_rates.append(player2 / player1)
print("Win rate average:", sum(win_rates)/len(win_rates))

#res = torneio(200, [chapiteau, jogador_26_v3, jogador_26_v4], 100)
#print(res)

#jogo = Kalah(0)
#_, _, res = joga11(jogo, jogador_26_v3, jogador_26_v4, True)
#print(res)