
from MedoTotal import *
from GrafoAbstracto import *

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