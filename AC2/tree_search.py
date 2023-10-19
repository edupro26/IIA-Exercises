
from MedoTotal import *

def depth_first_tree_search_all_count(problem,optimal=False,verbose=False):
    max_mem, visitados, final_states = 0, 0, []
    frontier = Stack()
    frontier.append(Node(problem.initial))

    while frontier:
        node = frontier.pop()
        visitados += 1
        if verbose:
            display_expand(node, problem)

        if problem.goal_test(node.state):
            final_states.append(node)
        else:
            max_mem = max(len(frontier), max_mem)
            if optimal and node.state.tempo == 1:
                frontier.extend(optimize(node, problem))
            else:
                frontier.extend(node.expand(problem))

    return (final_states[0], max_mem, visitados, len(final_states))


def display_expand(node, problem):
    print('---------------------\n')
    print(problem.display(node.state))
    if node.state.tempo == 0:
        print(f"GGGGooooooallllll --------- com o custo: {node.path_cost}")
    else:
        print(f"Custo: {node.path_cost}")


def optimize(node, problem):
    expanded = node.expand(problem)
    costs = []
    i = 0
    for node in expanded:
        if node.path_cost in costs:
            expanded.pop(i)
        costs.append(node.path_cost)
        i += 1
    return expanded