
from MedoTotal import *

def depth_first_tree_search_all_count(problem,optimal=False,verbose=False):
    visited, final_states = [], []
    reached_goal = False
    frontier = Stack()
    frontier.append(Node(problem.initial))

    while frontier:
        node = frontier.pop()
        print(node.state)
        visited.append(node)

        if verbose:
            print(problem.display(node.state))

        if problem.goal_test(node.state):
            reached_goal = True
            final_states.append(node)
            #return (node, None, visited, final_states)

        if not reached_goal:
            frontier.extend(node.expand(problem))

    return (final_states[0], None, len(visited), len(final_states))