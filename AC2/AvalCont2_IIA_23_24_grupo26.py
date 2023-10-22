"""
    Avaliação Contínua 2

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""

from collections import deque
from MedoTotal import *
from GrafoAbstracto import *


# ___________________________________________________________________________________
# Class MedoTotalTurbo (Pergunta 1)

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


# ___________________________________________________________________________________
# Method depth_first_tree_search_all_count() (Pergunta 2)

def depth_first_tree_search_all_count(problem, optimal=False, verbose=False):
    max_mem, visited, final_states = 0, 0, []
    frontier = [Node(problem.initial)]
    solution, solution_cost = None, float('inf')

    while frontier:
        max_mem = max(len(frontier), max_mem)
        node = frontier.pop()
        visited += 1
        if verbose:
            display_node(node, problem, None)

        expanded = node.expand(problem)
        if node.state.tempo > 1:
            expanded.reverse()

        if expanded:
            for node in expanded:
                if problem.goal_test(node.state):
                    if node.path_cost < solution_cost:
                        solution = node
                        solution_cost = node.path_cost
                    if not optimal:
                        visited = save_final_state(problem, node, solution, visited, final_states, verbose)
                    elif solution not in final_states:
                        visited = save_final_state(problem, node, solution, visited, final_states, verbose)
                else:
                    add_to_frontier(frontier, node, optimal, solution_cost)
    if solution:
        return (solution, max_mem, visited, len(final_states))
    else:
        return (None, max_mem, visited, len(final_states))


def save_final_state(problem, node, solution, visited, final_states, verbose):
    final_states.append(node)
    visited += 1
    if verbose:
        display_node(node, problem, solution)
    return visited


def add_to_frontier(frontier, node, optimal, solution_cost):
    if not optimal:
        frontier.append(node)
    else:
        if node.path_cost < solution_cost:
            frontier.append(node)


def display_node(node, problem, solution):
    print('---------------------\n')
    print(problem.display(node.state))
    if problem.goal_test(node.state):
        print(f"GGGGooooooallllll --------- com o custo: {node.path_cost}")
        if node == solution:
            print(f"Di best goal até agora")
    else:
        print(f"Custo: {node.path_cost}")


# ___________________________________________________________________________________
# Method ida_star_graph_search_count() (Pergunta 3)


def ida_star_graph_search_count(problem, f, verbose=False):
    initial = Node(problem.initial)
    cutOff, node_count, thresholds = f(initial), 0, set()
    while True:
        if verbose:
            print(f"------Cutoff at {cutOff}")
        goal = False
        frontier, visited, solution = [initial], {initial.state}, None
        node_count += 1
        while frontier:
            node = frontier.pop()
            display(verbose, problem, f, cutOff, node)
            if goal:
                display(verbose, problem, f, cutOff, None, solution)
                return (solution, node_count)
            if f(node) <= cutOff:
                child_nodes = node.expand(problem)
                child_nodes.reverse()
                new_cutOff = set()
                for child in child_nodes:
                    if child.state not in visited:
                        node_count += 1
                        visited.add(child.state)
                        if problem.goal_test(child.state):
                            goal, solution = get_best_solution(child, f, goal, solution, cutOff, new_cutOff)
                        else:
                            frontier.append(child)
                            if f(child) > cutOff:
                                new_cutOff.add(f(child))
                thresholds.update(new_cutOff)

        if solution:
            display(verbose, problem, f, cutOff, None, solution)

        cutOff = get_new_cutOff(thresholds)
        if cutOff == float('inf'):
            return (None, node_count)
        if verbose:
            print('\n')


def get_new_cutOff(thresholds):
    if thresholds:
        cutOff = min(thresholds)
        thresholds.remove(cutOff)
    else:
        cutOff = float('inf')
    return cutOff


def get_best_solution(child, f, goal, solution, cutOff, new_cutOff):
    if goal:
        if child.path_cost <= solution.path_cost:
            solution = child
    else:
        solution = child
    if f(solution) <= cutOff:
        goal = True
    else:
        new_cutOff.add(f(solution))
    return goal, solution


def display(verbose, problem, f, cutOff, node, solution=None):
    if verbose:
        if solution:
            if f(solution) <= cutOff:
                print()
                print(problem.display(solution.state))
                print("Cost:", solution.path_cost, "f=", f(solution))
                print("Goal found within cutoff!")
            else:
                print()
                print(problem.display(solution.state))
                print("Cost:", solution.path_cost, "f=", f(solution))
                print("Out of cutoff -- minimum out:", f(solution))
        elif f(node) <= cutOff:
            print()
            print(problem.display(node.state))
            print("Cost:", node.path_cost, "f=", f(node))
        else:
            print()
            print(problem.display(node.state))
            print("Cost:", node.path_cost, "f=", f(node))
            print("Out of cutoff -- minimum out:", f(node))