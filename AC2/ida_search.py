
from MedoTotal import *
from GrafoAbstracto import *


def ida_star_graph_search_count(problem, f, verbose=False):
    initial = Node(problem.initial)
    cutOff, node_count, thresholds = f(initial), 0, []
    while True:
        if verbose:
            print(f"------Cutoff at {cutOff}\n")
        frontier, visited, solution = [initial], [initial.state], False
        while frontier:
            node = frontier.pop()
            node_count += 1
            if verbose:
                display(problem, f, cutOff, node)
            if f(node) <= cutOff:
                child_nodes = node.expand(problem)
                child_nodes.reverse()
                for child in child_nodes:
                    if child.state not in visited:
                        if problem.goal_test(child.state):
                            solution = child
                            visited.append(child.state)
                            node_count += 1
                            if f(child) > cutOff and f(child) not in thresholds:
                                thresholds.append(f(child))
                        else:
                            frontier.append(child)
                            visited.append(child.state)
            elif f(node) not in thresholds:
                thresholds.append(f(node))

        if solution:
            if verbose:
                display(problem, f, cutOff, None, solution)
            if f(solution) > cutOff:
                solution = None
        else:
            if verbose:
                print()

        if thresholds:
            cutOff = min(thresholds)
            thresholds.remove(cutOff)
        else:
            cutOff = float('inf')

        if solution:
            return (solution, node_count)
        if cutOff == float('inf'):
            return (None, node_count)


def display(problem, f, cutOff, node, solution=None):
    if solution:
        if f(solution) <= cutOff:
            print(problem.display(solution.state))
            print("Cost:", solution.path_cost, "f=", f(solution))
            print("Goal found within cutoff!")
        else:
            print(problem.display(solution.state))
            print("Cost:", solution.path_cost, "f=", f(solution))
            print("Out of cutoff -- minimum out:", f(solution))
            print('\n')
    elif f(node) <= cutOff:
        print(problem.display(node.state))
        print("Cost:", node.path_cost, "f=", f(node))
        print()
    else:
        print(problem.display(node.state))
        print("Cost:", node.path_cost, "f=", f(node))
        print("Out of cutoff -- minimum out:", f(node))
        print()