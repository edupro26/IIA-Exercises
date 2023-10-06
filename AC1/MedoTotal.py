"""
    Avaliação Contínua 1 - MedoTotal

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""

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


# ___________________________________________________________________________________
# Class MedoTotal


class MedoTotal(Problem):

    def __init__(self, situacaoInicial=mundoStandard):
        self.grid = situacaoInicial
        self.grid_array = parse_grid(situacaoInicial)
        self.t = int(situacaoInicial.split('\n')[0][2:])
        self.m = int(situacaoInicial.split('\n')[1][2:])
        self.p = int(situacaoInicial.split('\n')[2][2:])

        inicial = {
            "T": self.t,
            "M": self.m,
            "pacman": find_pacman_position(self.grid_array),
            "super_pills": find_super_pills_positions(self.grid_array)
        }

        super().__init__(inicial)

    def actions(self, state):
        possible_directions = ["N", "W", "E", "S"]
        valid_actions = []

        if state["T"] > state["M"] and state["super_pills"] == []:
            return []

        (pacman_x, pacman_y) = state["pacman"]
        min_d_to_pill = min_distance_to_pill(pacman_x, pacman_y, self.grid_array)

        if min_d_to_pill == state["M"]:
            return []

        for direction in possible_directions:
            (new_x, new_y) = get_new_position(state["pacman"], direction)

            if self.grid_array[new_x][new_y] != "=" and self.grid_array[new_x][new_y] != "F":
                valid_actions.append(direction)

        return valid_actions

    def result(self, state, action):
        new_state = state

        (new_x, new_y) = get_new_position(state["pacman"], action)
        count = 0
        pill = False
        for (i, j) in new_state["super_pills"]:
            if (new_x, new_y) == (i, j):
                pill = True
                new_state["M"] = self.p
                new_state["super_pills"].remove((i,j))
                count += 1

        if pill:
            new_state["T"] -= 1
        else:
            new_state["T"] -= 1
            new_state["M"] -= 1

        new_state["pacman"] = (new_x, new_y)

        return new_state

    def path_cost(self, c, state1, action, next_state):
        pass

    def executa(self, state, actions):
        cost = 0
        for a in actions:
            nstate = self.result(state, a)
            #cost = self.path_cost(cost, state, a, nstate)
            state = nstate

        goal = self.goal_test(state)

        return state, cost, goal

    def display(self, state):
        self.grid_array = update_grid_with_state(self.grid_array, state)
        grid_string = ""
        for x in range(len(self.grid_array)):
            grid_string += " ".join(self.grid_array[x])
            if x < len(self.grid_array) - 1:
                grid_string += "\n"

        return grid_string.rstrip("\n")


# ___________________________________________________________________________________
# Auxiliar functions of MedoTotal class


def min_distance_to_pill(pacman_x, pacman_y, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = [(pacman_x, pacman_y, 0)]

    while queue:
        x, y, distance = queue.pop(0)

        if grid[x][y] == "*":
            return distance

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] != "=":
                queue.append((new_x, new_y, distance + 1))

    return None


def parse_grid(str):
    temp = str.split('\n')

    for i in range(len(temp)):
        temp[i] = temp[i].replace(' ', '')

    # Gets the grid of the state
    grid = [list(line) for line in temp[3:]]

    return grid


def find_pacman_position(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == "@":
                return (x, y)
    return (None, None)


def find_super_pills_positions(grid):
    super_pills = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == "*":
                super_pills.append((x, y))
    return super_pills


def update_grid_with_state(grid, state):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == "@":
                grid[x][y] = "."
            if grid[x][y] == "*":
                grid[x][y] = "."

    (new_x, new_y) = state["pacman"]
    grid[new_x][new_y] = "@"

    pills = state["super_pills"]
    for i in range(len(pills)):
        (px, py) = pills[i]
        grid[px][py] = "*"

    return grid


def get_new_position(pacman, direction):
    (new_x, new_y) = pacman

    if direction == "N":
        new_x -= 1
    elif direction == "S":
        new_x += 1
    elif direction == "E":
        new_y += 1
    elif direction == "W":
        new_y -= 1

    return (new_x, new_y)


g=MedoTotal()
seq=['S', 'S', 'S', 'S', 'S', 'S', 'S', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'S', 'S', 'S', 'S', 'S']
final,custo,goal=g.executa(g.initial,seq)
print(final)
print(g.display(final))
print('Custo total:',custo)
print('Goal?',g.goal_test(final))