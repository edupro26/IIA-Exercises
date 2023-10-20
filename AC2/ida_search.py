from MedoTotal import * 
from GrafoAbstracto import *

def ida_star_graph_search_count(problem, f, verbose=False):
    initial_cutoff = f(Node(problem.initial))
    states_seen = set()
    node_count = 0
    while True:
        if verbose:
            print("------Cutoff set to", initial_cutoff)
        node = Node(problem.initial)
        print(node.state)
        print("Cost:", 0, "f=", f(node))
        print("")
        solution_node, new_cutoff = recursive_dfs(node, initial_cutoff, problem, states_seen, verbose, node_count)
        
        if solution_node:
            return solution_node, node_count
        
        if new_cutoff == float('inf'):
            return None, node_count
        
        initial_cutoff = new_cutoff

def recursive_dfs(current_node, cutoff, problem, states_seen, verbose, node_count):
        states_seen.add(current_node.state)
        node_count += 1
        
        f_value = f(current_node)
        
        if f_value > cutoff:
            return None, f_value
        
        if problem.goal_test(current_node.state):
            return current_node, float('inf')
        
        next_cutoff = float('inf')
        
        #print(problem.actions(current_node.state))
        c_nodes = []
        for move in problem.actions(current_node.state):
            successor_state = problem.result(current_node.state, move)
            
            if successor_state in states_seen:
                continue
            move_cost = problem.path_cost(current_node.path_cost, current_node.state, move, successor_state)
            successor_node = Node(successor_state, current_node, move, move_cost)
            
            if verbose:
                print(successor_node.state)
                print("Cost:", move_cost, "f=", f(successor_node))
                print("")
            #found_node, new_cutoff = recursive_dfs(successor_node, cutoff)
            c_nodes.append((successor_node, cutoff))
        for x in reversed(c_nodes):
            found_node, new_cutoff = recursive_dfs(x[0], x[1], problem, states_seen, verbose, node_count)
            if found_node:
                return found_node, float('inf')
            next_cutoff = min(next_cutoff, new_cutoff)
        
        return None, next_cutoff

s = ProblemaGrafo()
print('---------------- IDA* pedagógico ----------------')
f=lambda n: n.path_cost + s.h1(n)
res_IDAstar,visitados=ida_star_graph_search_count(s,f,True)
if res_IDAstar:
    print("\nSolução:",res_IDAstar.solution(),'com custo',res_IDAstar.path_cost)
else:
    print('\nSem Solução')
print('Visitados:',visitados)