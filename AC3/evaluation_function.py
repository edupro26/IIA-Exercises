"""
    Avaliação Contínua 3

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""

from tournament import *


# ______________________________________________________________________________
# Evaluation functions


def func_26_v4(state, player):
    value = 0
    if state.is_game_over():
        result = state.result()
        return result*100 if player == state.SOUTH else result*-100

    south_score = state.state[state.SOUTH_SCORE_PIT]
    north_score = state.state[state.NORTH_SCORE_PIT]
    for pit in range(state.PLAY_PITS):
        if player == state.SOUTH:
            score_pit = state.SOUTH_SCORE_PIT
            if score_pit - pit == state.state[pit]:
                value += 1
            final_pit = pit+state.state[pit]
            if state.state[pit] > 0 and 0 <= final_pit < score_pit:
                if state.state[final_pit] == 0:
                    value += (1 + state.state[2*state.PLAY_PITS-final_pit])
            value += (south_score - north_score)
        else:
            score_pit = state.NORTH_SCORE_PIT
            pit += state.PLAY_PITS+1
            if score_pit - pit == state.state[pit]:
                value += 1
            final_pit = pit + state.state[pit]
            if state.state[pit] > 0 and state.PLAY_PITS+1 <= final_pit < score_pit:
                if state.state[final_pit] == 0:
                    value += (1 + state.state[2*state.PLAY_PITS-final_pit])
            value += (north_score - south_score)
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


def func_26_v2(state, player):
    if state.is_game_over():
        winner = state.result()
        return winner * 100 if player == state.SOUTH else winner * -100

    south_sum, north_sum = 0, 0
    for i in range(state.PLAY_PITS+1):
        south_sum += state.state[i]
        north_sum += state.state[i+7]

    if player == state.SOUTH:
        utility = 0
        score_pit = state.SOUTH_SCORE_PIT
        for i in range(state.PLAY_PITS):
            if score_pit - i == state.state[i]:
                utility += 10
        value = (south_sum - north_sum)
        if south_sum >= north_sum:
            value += utility
    else:
        utility = 0
        score_pit = state.NORTH_SCORE_PIT
        for i in range(state.PLAY_PITS):
            if score_pit - (i+7) == state.state[i+7]:
                utility += 10
        value = (north_sum - south_sum)
        if north_sum >= south_sum:
            value += utility

    return value


def func_26(state, player):
    if state.is_game_over():
        winner = state.result()
        return winner * 100 if player == state.SOUTH else winner * -100

    south_sum, north_sum = 0, 0
    for i in range(state.PLAY_PITS+1):
        south_sum += state.state[i]
        north_sum += state.state[i+7]

    if player == state.SOUTH:
        value = south_sum - north_sum
    else:
        value = north_sum - south_sum

    return value


# ______________________________________________________________________________
# TESTS

#el_caos_int3=JogadorAlfaBeta("El Caos Inteligente 3",3,f_caos_intel)
#el_caos_int6=JogadorAlfaBeta("El Caos Inteligente 6",6,f_caos_intel)
#el_caos_int2=JogadorAlfaBeta("El Caos Inteligente 2",2,f_caos_intel)
chapiteau = JogadorAlfaBeta("Chapiteau", 3, chapiteau_replica)
jogador_26_v1=JogadorAlfaBeta("Jogador26_v1", 3, func_26)
jogador_26_v2=JogadorAlfaBeta("Jogador26_v2", 3, func_26_v2)
jogador_26_v3=JogadorAlfaBeta("Jogador26_v3", 3, func_26_v3)
jogador_26_v4=JogadorAlfaBeta("Jogador26_v4", 3, func_26_v4)

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
#jogo=Kalah(100)
#_,_,res,s = jogaNpares(jogo,100, jogador_26_v3, jogador_26_v4)
#print(res,s)

#res = torneio(100,[chapiteau,jogador_26_v3,jogador_26_v4],10)
#print(res)

#res = torneio(200,[jogador_26_v1,jogador_26_v2,jogador_26_v3,jogador_26_v4],100)
#print(res)

res = torneio(300,[jogador_26_v3,jogador_26_v4],10)
print(res)