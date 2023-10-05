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
        t = int(parametros.split('\n')[0][2:])
        m = int(parametros.split('\n')[1][2:])
        grid = self.parse_grid(state)

        # Pacman's position
        pacman_x, pacman_y = self.find_pacman_position(grid)

        min_d_to_pill = self.min_distance_to_pill(pacman_x, pacman_y, grid)

        if min_d_to_pill > int(parametros.split('\n')[2][2:]) - 1 and t > m:
            return []
        
        if min_d_to_pill == m:
            return []

        possible_directions = ["N", "W", "E", "S"]
        valid_actions = []

        for direction in possible_directions:
            new_x, new_y = self.get_new_position(pacman_x, pacman_y, direction)

            if self.is_valid_position(new_x, new_y, grid, t):
                valid_actions.append(direction)

        return valid_actions

    def result(self, state, action):
        new_state = state
        t = int(parametros.split('\n')[0][2:]) - 1
        m = int(parametros.split('\n')[1][2:]) - 1
        p = int(parametros.split('\n')[2][2:])

        grid = self.parse_grid(state)
        pacman_x, pacman_y = self.find_pacman_position(grid)

        new_x, new_y = self.get_new_position(pacman_x, pacman_y, action)

        grid[pacman_x][pacman_y] = "."
        grid[new_x][new_y] = "@"

        # Remakes the new state
        new_state_lines = [f"T={t}\nM={m}\nP={p}"] + [' '.join(line) for line in grid]
        new_state = '\n'.join(new_state_lines)

        return new_state


    def path_cost(self, c, state1, action, next_state):

        if next_state not in state1:
            action_cost = 1
        else:
            action_cost = state1[next_state] + 1
        
        return c + action_cost

    def executa(self, state, actions):
        """Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado"""
        nstate = state
        for a in actions:
            nstate = self.result(nstate, a)

        custo = self.path_cost(0, state, actions, nstate)
        goal = self.goal_test(nstate)
        return nstate, custo, goal

    def display(self, state):
        """Devolve a grelha em modo txt"""
        return state[len(parametros) + 1:len(state)]


    # Auxiliar functions of MedoTotal class

    def is_valid_position(self, x, y, grid, T):
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            if grid[x][y] != "=" and grid[x][y] != "F":
                if grid[x][y] != "." and grid[x][y] != "*":
                    visited_count = int(grid[x][y])
                    if visited_count < T:
                        return True
                else:
                    return True
        return False


    def parse_grid(self, state):
        state_lines = state.split('\n')

        for i in range(len(state_lines)):
            state_lines[i] = state_lines[i].replace(' ', '')

        # Gets the grid of the state
        grid = [list(line) for line in state_lines[3:]]

        return grid

    def find_pacman_position(self, grid):
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] == "@":
                    return x, y
        return None, None

    def get_new_position(self, x, y, direction):
        new_x, new_y = x, y

        if direction == "N":
            new_x -= 1
        elif direction == "S":
            new_x += 1
        elif direction == "E":
            new_y += 1
        elif direction == "W":
            new_y -= 1

        return new_x, new_y
    
    def min_distance_to_pill(self, pacman_x, pacman_y, grid):
        queue = [(pacman_x, pacman_y, 0)]

        visited = set()
        visited.add((pacman_x, pacman_y))

        while queue:
            x, y, distance = queue.pop(0)

            if grid[x][y] == "*":
                return distance

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy

                if (
                    0 <= new_x < len(grid)
                    and 0 <= new_y < len(grid[0])
                    and grid[new_x][new_y] != "="
                    and (new_x, new_y) not in visited
                ):
                    queue.append((new_x, new_y, distance + 1))
                    visited.add((new_x, new_y))

        return float('inf')
