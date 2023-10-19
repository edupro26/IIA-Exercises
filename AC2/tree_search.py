
from MedoTotal import *

def depth_first_tree_search_all_count(problem,optimal=False,verbose=False):
    final_states = []
    visitados, max_mem = 0, 0
    frontier = Stack()
    frontier.append(Node(problem.initial))

    while frontier:
        node = frontier.pop()
        visitados += 1

        if verbose:
            print(problem.display(node.state))

        if problem.goal_test(node.state):
            final_states.append(node)
        else:
            if len(frontier) > max_mem:
                max_mem = len(frontier)

            frontier.extend(node.expand(problem))

    return (final_states[0], max_mem, visitados, len(final_states))


parametros="T=6\nM=4\nP=10"
linha1= "= = = = = =\n"
linha2= "= . @ F * =\n"
linha3= "= . . . . =\n"
linha4= "= . = . . =\n"
linha5= "= . = . . =\n"
linha6= "= = = = = =\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6
mundoStandardx=parametros + "\n" + grelha
gx=MedoTotal(mundoStandardx)

resultado,max_mem,visitados,finais = depth_first_tree_search_all_count(gx)
print('*'*20)
if resultado:
    print("Solução Prof-total (árvore) com custo " + str(resultado.path_cost)+":")
    print(resultado.solution())
else:
    print('\nSem Solução')
print('Visitados=',visitados)
print('Dimensão máxima da memória',max_mem)
print('Estados finais:',finais)