
from MedoTotal import *
from GrafoAbstracto import *


def ida_star_graph_search_count(problem, f, verbose=False):
    cutOff = f(Node(problem.initial))
    visited, out = 0, []
    solution, current_solution = None, None

    while not solution:
        display_node(problem, current_solution, f, cutOff, verbose, solution)
        visited += 1
        if out:
            cutOff = min(out)
            if verbose:
                print()
        if verbose:
            print(f"------Cutoff at {cutOff}\n")
        goal_found = False
        frontier = [Node(problem.initial)]
        while frontier:
            node = frontier.pop()
            display_node(problem, node, f, cutOff, verbose, solution)
            visited += 1
            if f(node) <= cutOff:
                if not goal_found:
                    expanded = node.expand(problem)
                    expanded = teste(cutOff, expanded, f)
                    expanded.reverse()
                    for child in expanded:
                        if problem.goal_test(child.state):
                            goal_found = True
                            if f(child) <= cutOff:
                                solution = child
                            else:
                                current_solution = child
                                out.append(f(child))
                        else:
                            frontier.append(child)
            else:
                out.append(f(node))

    display_node(problem, solution, f, cutOff, verbose, solution)
    return (solution, visited)


def teste(cutOff, expanded, f):
    in_cutOff = False
    for child in expanded:
        if f(child) < cutOff:
            in_cutOff = True

    if in_cutOff:
        return expanded
    else:
        return []


def display_node(problem, node, f, cutOff, verbose, solution):
    if verbose and node:
        if f(node) <= cutOff:
            if node == solution:
                print(problem.display(node.state))
                print("Cost:", node.path_cost, "f=", f(node))
                print("Goal found within cutoff!")
            else:
                print(problem.display(node.state))
                print("Cost:", node.path_cost, "f=", f(node))
                print()
        else:
            print(problem.display(node.state))
            print("Cost:", node.path_cost, "f=", f(node))
            print("Out of cutoff -- minimum out:", f(node))
            print()