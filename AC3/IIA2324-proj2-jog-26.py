"""
    Avaliação Contínua 3

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""


from kalah import *
from jogos import *
from fairKalahs import *
from utils import *


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


# This code might not be the exact chapiteau code
def chapiteau_replica(estado, jogador):
    ret = 0
    if jogador == estado.SOUTH:
        for i in range(6):
            ret += estado.state[i]
            ret -= estado.state[7 + i]
    else:
        for i in range(6):
            ret -= estado.state[i]
            ret += estado.state[7 + i]
    if estado.is_game_over():
        aux = estado.result()
        return aux * 100 if jogador == estado.SOUTH else aux * -100
    return ret


def f_caos_intel(estado,jogador):
    """Quando é terminal: +100 para vitória, -100 para a derrota e 0 para o empate.
       Quando o tabuleiro é não terminal devolve 0, o que quer dizer que como o minimax baralha as acções, será random"""
    if estado.is_game_over():
        aux = estado.result()
        return aux*100 if jogador == estado.SOUTH else aux*-100
    return 0


# ______________________________________________________________________________
# Players

class Jogador():
    def __init__(self, nome, fun):
        self.nome = nome
        self.fun = fun

    def display(self):
        print(self.nome + " ")


class JogadorAleat(Jogador):
    def __init__(self, nome):
        self.nome = nome
        self.fun = lambda game, state: random.choice(game.actions(state))


class JogadorAlfaBeta(Jogador):
    def __init__(self, nome, depth, fun_eval):
        self.nome = nome
        self.fun = lambda game, state: alphabeta_cutoff_search_new(state, game, depth, eval_fn=fun_eval)


# ______________________________________________________________________________
# 1v1 function


##########  para ser independente dos jogos deveria devolver um método em string ou um atributo
def joga11(game, jog1, jog2,verbose=False):
    ### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
    ### devolve o par de jogadores, a lista de jogadas e o resultado
    estado=game.initial
    proxjog = jog1
    lista_jogadas=[]
    lance = 0
    while not game.terminal_test(estado):
        if verbose:
            print('----------   LANCE:',lance)
            game.display(estado)
        jogada = proxjog.fun(game, estado)
        if verbose:
            print('JOGADA=',jogada)
        estado=game.result(estado,jogada)
        lista_jogadas.append(jogada)
        proxjog = jog2 if proxjog == jog1 else jog1
        lance+=1
    #p jogou e ganhou
    util=game.utility(estado,0)
    if util == 1:
        resultado=jog1.nome
    elif util== -1:
        resultado = jog2.nome
    else:
        resultado='Empate'
    return ((jog1.nome,jog2.nome),lista_jogadas,resultado)


# ______________________________________________________________________________
# Tournament functions


scores={'Vitoria': 3, 'Empate': 1}

def traduzPontos(tabela):
    tabelaScore={}
    empates=tabela['Empate']
    for x in tabela:
        if x != 'Empate':
            tabelaScore[x]=scores['Vitoria']*tabela[x]+empates
    return tabelaScore

def jogaNpares(jogo,n,jog1,jog2):
    tabelaPrim={jog1.nome:0, jog2.nome:0, 'Empate':0}
    tabelaSeg={jog1.nome:0, jog2.nome:0, 'Empate':0}
    tabela={}
    for _ in range(n):
        _,_,vencedor=joga11(jogo,jog1,jog2)
        tabelaPrim[vencedor]+=1
        _,_,vencedor=joga11(jogo,jog2,jog1)
        tabelaSeg[vencedor]+=1
    for x in tabelaPrim:
        tabela[x]=tabelaPrim[x]+tabelaSeg[x]
    return tabelaPrim,tabelaSeg,tabela,traduzPontos(tabela)


def incorpora(tabela, tx):
    for jog in tx:
        if jog not in tabela:
            tabela[jog] = tx[jog]
        else:
            tabela[jog] += tx[jog]


def torneio(n, jogadores, jogo_id=0):
    jogo = Kalah(jogo_id)  # jogo gerado ao calha entre os "justos"
    tabela = {}
    for i in range(len(jogadores) - 1):
        jog1 = jogadores[i]
        for j in range(i + 1, len(jogadores)):
            jog2 = jogadores[j]
            _, _, _, tabelaX = jogaNpares(jogo, n, jog1, jog2)
            incorpora(tabela, tabelaX)
    return tabela


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

#res = torneio(200,[chapiteau,jogador_26_v1,jogador_26_v4],0)
#print(res)

res = torneio(200,[jogador_26_v1,jogador_26_v2,jogador_26_v3,jogador_26_v4],100)
print(res)