
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
        self.grid = self.parse_grid()
        super().__init__(board)

    def falha_antecipada(self, state):
        if state.medo < state.tempo:
            if state.pastilhas == set():
                return True
            #TODO

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
                new_x = current[0] + move[0]
                new_y = current[1] + move[1]
                new_pos = (new_x, new_y)

                if 0 <= new_x < self.dim and 0 <= new_y < self.dim and new_pos not in visited:
                    if self.grid[new_x][new_y] not in ['=', 'F']:
                        queue.append((new_pos, distance + 1))
                        visited.add(new_pos)

        return -1

    def parse_grid(self):
        grid = grelha.strip().split('\n')
        for i in range(len(grid)):
            grid[i] = grid[i].replace(' ', '')

        grid = [list(row) for row in grid]

        return grid