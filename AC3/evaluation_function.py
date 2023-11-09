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
        return result*100 if player == state.SOUTH else result*-100

    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    h1 = (south_score - north_score) if player == state.SOUTH else (north_score - south_score)
    h2 = south_score if player == state.SOUTH else north_score
    h3 = winningDistance(state, player, south_score, north_score)
    h4 = piecesInPits(state, player)
    h5 = countNonEmptyPits(state, player)
    h6 = extraMove(state, player)
    #h7 = pieceSteals(state, player) #This heuristic might not be needed
    #h8 = leftMostPit(state, player) #Still needs testing

    return (h1*0.5)+(h2*0.1)+(h3*0.15)+(h4*0.03)+(h5*0.02)+(h6*0.2)


def leftMostPit(state, player):
    value = 0
    if player == state.SOUTH:
        value += state.state[0]
    else:
        value += state.state[0+state.PLAY_PITS+1]
    return value


def pieceSteals(state, player):
    value = 0
    if player == state.SOUTH:
        score_pit = state.SOUTH_SCORE_PIT
        for i in range(state.PLAY_PITS):
            pit = i
            if state.state[pit] > 0:
                final_pit = pit + state.state[pit]
                if 0 <= final_pit < score_pit:
                    if state.state[pit] == 0:
                        value += (1 + state.state[2 * state.PLAY_PITS - final_pit])
    else:
        score_pit = state.NORTH_SCORE_PIT
        for i in range(state.PLAY_PITS):
            pit = i + state.PLAY_PITS+1
            if state.state[pit] > 0:
                final_pit = pit + state.state[pit]
                if 0 <= final_pit < score_pit:
                    if state.state[pit] == 0:
                        value += (1 + state.state[2 * state.PLAY_PITS - final_pit])
    return value


def extraMove(state, player):
    value = 0
    if player == state.SOUTH:
        score_pit = state.SOUTH_SCORE_PIT
        for i in range(state.PLAY_PITS):
            pit = i
            if score_pit - pit == state.state[pit]:
                value += 1
    else:
        score_pit = state.NORTH_SCORE_PIT
        for i in range(state.PLAY_PITS):
            pit = i + state.PLAY_PITS+1
            if score_pit - pit == state.state[pit]:
                value += 1
    return value


def winningDistance(state, player, s_score, n_score):
    value = 0
    if player == state.SOUTH:
        value += -((n_score*1.5) - s_score)
    else:
        value += -((s_score*1.5) - n_score)
    return value


def countNonEmptyPits(state, player):
    value = 0
    if player == state.SOUTH:
        for i in range(state.PLAY_PITS):
            if state.state[i] > 0:
                value += 1
    else:
        for i in range(state.PLAY_PITS):
            if state.state[i + state.PLAY_PITS+1] > 0:
                value += 1
    return value


def piecesInPits(state, player):
    value = 0
    if player == state.SOUTH:
        for i in range(state.PLAY_PITS):
            value += state.state[i]
    else:
        for i in range(state.PLAY_PITS):
            value += state.state[i + state.PLAY_PITS+1]
    return value


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

el_caos_int=JogadorAlfaBeta("El Caos Inteligente 6",6,f_caos_intel)
chapiteau = JogadorAlfaBeta("Chapiteau", 2, chapiteau_replica)
jogador_26_v3=JogadorAlfaBeta("Jogador26_v3", 2, func_26_v3)
jogador_26_v4=JogadorAlfaBeta("Jogador26_v4", 2, func_26_v4)

#for i in range(100):
#    jogo=Kalah(i)
#    _, _, res, s = jogaNpares(jogo, 10, jogador_26_v3, jogador_26_v4)
#    print(res, s)

#jogo=Kalah(0)
#_,_,res,s = jogaNpares(jogo,100, jogador_26_v3, jogador_26_v4)
#print(res,s)
#
#jogo=Kalah(50)
#_,_,res,s = jogaNpares(jogo,100, jogador_26_v3, jogador_26_v4)
#print(res,s)
#
#jogo=Kalah(10)
#_,_,res,s = jogaNpares(jogo,100, el_caos_int, jogador_26_v4)
#print(res,s)

#res = torneio(300,[chapiteau,jogador_26_v3,jogador_26_v4],10)
#print(res)

res = torneio(500,[jogador_26_v3,jogador_26_v4], 10)
print(res)