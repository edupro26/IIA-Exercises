from kalah import *
from jogos import *
from fairKalahs import *
from utils import *

class Jogador():
    def __init__(self, nome, fun):
        self.nome = nome
        self.fun = fun
    def display(self):
        print(self.nome+" ")
        
class JogadorAleat(Jogador):
    def __init__(self, nome):
        self.nome = nome
        self.fun = lambda game, state: random.choice(game.actions(state))

class JogadorAlfaBeta(Jogador):
    def __init__(self, nome, depth,fun_eval):
        self.nome = nome
        self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)

def f_caos_intel(estado,jogador):
    """Quando é terminal: +100 para vitória, -100 para a derrota e 0 para o empate.
       Quando o tabuleiro é não terminal devolve 0, o que quer dizer que como o minimax baralha as acções, será random"""
    if estado.is_game_over():
        aux = estado.result()
        return aux*100 if jogador == estado.SOUTH else aux*-100
    return 0

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

# Função para avaliar o estado do jogo
def evaluate(state):
    if state.is_game_over():
        result = state.result()
        if result == 0:
            return 0
        elif result == -1:
            return -1000
        else:
            return 1000
    else:
        north_score = state.state[KalahState.NORTH_SCORE_PIT]
        south_score = state.state[KalahState.SOUTH_SCORE_PIT]

        # Considere o número de sementes em cada poço para ambos os jogadores
        north_seeds = sum(state.state[KalahState.NORTH_PITS])
        south_seeds = sum(state.state[KalahState.SOUTH_PITS])

        # Peso para o equilíbrio de sementes
        balance_weight = 0.5

        # Avaliação ponderada
        score = (north_score - south_score) + balance_weight * (north_seeds - south_seeds)

        return score




# Função de estratégia
def func_26(game, state):
    def minimax(state, depth, maximizing_player):
        if depth == 0 or game.terminal_test(state):
            return evaluate(state)

        legal_moves = game.actions(state)
        if maximizing_player:
            best_value = float('-inf')
            for move in legal_moves:
                clone_state = game.result(state, move)
                value = minimax(clone_state, depth - 1, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for move in legal_moves:
                clone_state = game.result(state, move)
                value = minimax(clone_state, depth - 1, True)
                best_value = min(best_value, value)
            return best_value

    player = state.to_move
    legal_moves = game.actions(state)
    if not legal_moves:
        return None  # Sem movimentos possíveis

    best_move = legal_moves[0]
    best_score = float('-inf')

    for move in legal_moves:
        clone_state = state.real_move(move)
        score = minimax(clone_state, depth=4, maximizing_player=(player == state.to_move))

        if score > best_score:
            best_move = move
            best_score = score

    return best_move





el_caos = JogadorAleat("El Caos")
func_26_player = JogadorAleat("func_26")
el_caos_int6=JogadorAlfaBeta("El Caos Inteligente 6",6,f_caos_intel)

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

jogo=Kalah(10)
result = jogaNpares(jogo, 100, el_caos_int6, func_26_player)
print(result)

# Crie uma instância de Kalah para jogar
#game = Kalah(20)

# Crie instâncias dos jogadores
#el_caos = JogadorAleat("El Caos")
#func_26_player = JogadorAleat("func_26")

# Realize um jogo entre os jogadores
#_, _, resultado = joga11(game, func_26_player, el_caos)

# Exiba o resultado do jogo
#print("Resultado:", resultado)




# Se desejar, pode criar mais funções auxiliares ou testes aqui

# Exemplo de uso
#if __name__ == "__main__":
#    game = Kalah()
#    state = game.initial
#    game.display(state)
#    while not game.terminal_test(state):
#        move = func_26(game, state)
#        if move is not None:
#            state = game.result(state, move)
#            game.display(state)
#        else:
#            print("Nenhum movimento disponível. O jogo terminou.")
#            break