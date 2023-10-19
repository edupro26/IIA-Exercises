
from MedoTotal import *

def depth_first_tree_search_all_count(problem, optimal=False, verbose=False):
    max_mem, visitados, final_states = 0, 0, []
    frontier = Stack()
    frontier.append(Node(problem.initial))
    best_solution = None

    while frontier:
        max_mem = max(len(frontier), max_mem)
        node = frontier.pop()
        visitados += 1
        if verbose:
            display_expand(node, problem, best_solution)

        expanded = node.expand(problem)
        if node.state.tempo != 1:
            expanded.reverse()

        for node in range(len(expanded)):
            if problem.goal_test(expanded[node].state):
                if best_solution is None or expanded[node].path_cost < best_solution.path_cost:
                    best_solution = expanded[node]

                if optimal:
                    if best_solution not in final_states:
                        final_states.append(best_solution)
                        visitados += 1
                        if verbose:
                            display_expand(expanded[node], problem, best_solution)
                else:
                    final_states.append(expanded[node])
                    visitados += 1
                    if verbose:
                        display_expand(expanded[node], problem, best_solution)
            else:
                frontier.append(expanded[node])

    return (best_solution, max_mem, visitados, len(final_states))


def display_expand(node, problem, best_solution):
    print('---------------------\n')
    print(problem.display(node.state))
    if node.state.tempo == 0:
        print(f"GGGGooooooallllll --------- com o custo: {node.path_cost}")
        if node == best_solution:
            print(f"Di best goal até agora")
    else:
        print(f"Custo: {node.path_cost}")




#def depth_first_tree_search_all_count(problem,optimal=False,verbose=False):
#    max_mem, visitados, final_states = 0, 0, []
#    frontier = Stack()
#    frontier.append(Node(problem.initial))
#
#    while frontier:
#        max_mem = max(len(frontier), max_mem)
#        node = frontier.pop()
#        visitados += 1
#        if verbose:
#            display_expand(node, problem)
#
#        if problem.goal_test(node.state):
#            final_states.append(node)
#        else:
#            expanded = node.expand(problem)
#            expanded.reverse()
#            if optimal and node.state.tempo == 1:
#                optimize(expanded, frontier)
#            else:
#                if node.state.tempo > 1:
#                    frontier.extend(expanded)
#
#    return (get_best_solution(final_states), max_mem, visitados, len(final_states))


#def optimize(expanded, frontier):
#    costs = []
#    i = 0
#    for node in expanded:
#        if node.path_cost in costs:
#            expanded.pop(i)
#        costs.append(node.path_cost)
#        i += 1
#    frontier.extend(expanded)