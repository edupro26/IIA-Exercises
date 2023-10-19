
from MedoTotal import *


def depth_first_tree_search_all_count(problem, optimal=False, verbose=False):
    max_mem, visited, final_states = 0, 0, []
    frontier = [Node(problem.initial)]
    while frontier:
        max_mem = max(len(frontier), max_mem)
        node = frontier.pop()
        visited += 1
        if verbose:
            display_node(node, problem, None)

        expanded = node.expand(problem)
        if expanded:
            if problem.goal_test(expanded[0].state):
                solution = expanded[0]
                solution, visited, final_states = search_solutions(problem, expanded, solution, visited,
                                                                   optimal, verbose)
                return (solution, max_mem, visited, len(final_states))

        expanded.reverse()
        frontier.extend(expanded)
    return (None, max_mem, visited, len(final_states))


def search_solutions(problem, expanded, solution, visited, optimal, verbose):
    final_states = []
    for node in expanded:
        if node.path_cost < solution.path_cost:
            solution = node
        if not optimal:
            final_states.append(node)
            visited += 1
            if verbose:
                display_node(node, problem, solution)
        elif solution not in final_states:
            final_states.append(node)
            visited += 1
            if verbose:
                display_node(node, problem, solution)
    return solution, visited, final_states


def display_node(node, problem, solution):
    print('---------------------\n')
    print(problem.display(node.state))
    if problem.goal_test(node.state):
        print(f"GGGGooooooallllll --------- com o custo: {node.path_cost}")
        if node == solution:
            print(f"Di best goal até agora")
    else:
        print(f"Custo: {node.path_cost}")