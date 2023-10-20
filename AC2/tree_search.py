
from MedoTotal import *


def depth_first_tree_search_all_count(problem, optimal=False, verbose=False):
    max_mem, visited, final_states = 0, 0, []
    frontier = [Node(problem.initial)]
    solution = None
    solution_cost = float('inf')

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
                        final_states.append(node)
                        visited += 1
                        if verbose:
                            display_node(node, problem, solution)
                    elif solution not in final_states:
                        final_states.append(node)
                        visited += 1
                        if verbose:
                            display_node(node, problem, solution)
                else:
                    if not optimal:
                        frontier.append(node)
                    else:
                        if node.path_cost < solution_cost:
                            frontier.append(node)
    if solution:
        return (solution, max_mem, visited, len(final_states))
    else:
        return (None, max_mem, visited, len(final_states))

def display_node(node, problem, solution):
    print('---------------------\n')
    print(problem.display(node.state))
    if problem.goal_test(node.state):
        print(f"GGGGooooooallllll --------- com o custo: {node.path_cost}")
        if node == solution:
            print(f"Di best goal até agora")
    else:
        print(f"Custo: {node.path_cost}")