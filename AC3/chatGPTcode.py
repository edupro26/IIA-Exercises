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