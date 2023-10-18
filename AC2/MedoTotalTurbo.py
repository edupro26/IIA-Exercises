
from collections import deque
from MedoTotal import *

parametros="T=26\nM=6\nP=10"
linha1= "= = = = = = = = = =\n"
linha2= "= @ . * . . * . . =\n"
linha3= "= . = = = = = = . =\n"
linha4= "= . = F . . . . . =\n"
linha5= "= . = . . . . . . =\n"
linha6= "= . = . . . . . . =\n"
linha7= "= . = . . . . . . =\n"
linha8= "= * . . . . . . . =\n"
linha9= "= . . . . . . . . =\n"
linha10="= = = = = = = = = =\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9+linha10
mundoStandard=parametros + "\n" + grelha

class MedoTotalTurbo(MedoTotal):

    def __init__(self, board=mundoStandard):
        super().__init__(board)
        self.real_distances = self.store_distances()

    def store_distances(self):
        real_distances = {}
        for i in range(self.dim):
            for j in range(self.dim):
                if (i, j) not in self.obstacles and (i, j) != self.fantasma:
                    real_distances[(i, j)] = {}
                    for pill in self.initial.pastilhas:
                        distance = self.real_distance((i, j), pill)
                        real_distances[(i, j)][pill] = distance

        return real_distances

    def falha_antecipada(self, state):
        if state.tempo > state.medo:
            if state.pastilhas == set():  # se não há mais pastilhas e eram necessárias
                return True

            min_distance = min(self.real_distances[state.pacman][pill] for pill in state.pastilhas)
            if min_distance > state.medo:  # Se não há tempo (real_distance) para chegar à próxima super-pastilha
                return True

            if (state.medo + self.poder * len(state.pastilhas)) < state.tempo:
                # se o poder de todas as pastilhas mais o medo são insuficientes.
                return True

        return False


    def real_distance(self, start, pill):
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        queue = deque([(start, 0)])
        visited = set()

        while queue:
            current, distance = queue.popleft()
            if current == pill:
                return distance

            for move in moves:
                new_x = current[1] + move[1]
                new_y = current[0] + move[0]
                new_pos = (new_y, new_x)

                if 0 <= new_x < self.dim and 0 <= new_y < self.dim and new_pos not in visited:
                    if new_pos != self.fantasma and new_pos not in self.obstacles:
                        queue.append((new_pos, distance + 1))
                        visited.add(new_pos)

        return -1