
from MedoTotal import *

def depth_first_tree_search_all_count(problem,optimal=False,verbose=False):
    final_states = []
    visitados = 0
    frontier = Stack()
    frontier.append(Node(problem.initial))

    while frontier:
        node = frontier.pop()
        print(node.state)
        visitados += 1

        if verbose:
            print(problem.display(node.state))

        if problem.goal_test(node.state):
            final_states.append(node)
        else:
            frontier.extend(node.expand(problem))

    return (final_states[0], None, visitados, len(final_states))