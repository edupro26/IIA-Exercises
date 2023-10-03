from searchPlus import *

parametros = "T=26\nM=6\nP=10"
linha1 = "= = = = = = = = = =\n"
linha2 = "= @ . * . . * . . =\n"
linha3 = "= . = = = = = = . =\n"
linha4 = "= . = F . . . . . =\n"
linha5 = "= . = . . . . . . =\n"
linha6 = "= . = . . . . . . =\n"
linha7 = "= . = . . . . . . =\n"
linha8 = "= * . . . . . . . =\n"
linha9 = "= . . . . . . . . =\n"
linha10 = "= = = = = = = = = =\n"
grelha = linha1 + linha2 + linha3 + linha4 + linha5 + linha6 + linha7 + linha8 + linha9 + linha10
mundoStandard = parametros + "\n" + grelha


class MedoTotal(Problem):

    def __init__(self, situacaoInicial=mundoStandard):
        super().__init__(initial=situacaoInicial)
        self.situacaoInicial = situacaoInicial

    def actions(self, state):
        # TODO
        pass

    def result(self, state, action):
        # TODO
        pass

    def path_cost(self, c, state1, action, next_state):
        # TODO
        pass

    def executa(self, state, actions):
        """Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado"""
        nstate = state
        for a in actions:
            nstate = p.result(nstate, a)
        return nstate

    def display(self, state):
        """Devolve a grelha em modo txt"""
        return state[len(parametros)+1:len(state)]