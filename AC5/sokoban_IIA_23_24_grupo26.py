"""
    Avaliação Contínua 5

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""


from planningPlus import *
from logic import *
from utils import *
from search import *


def sokoban(puzzle):
    pass


# ____________________________________________________________________
# TESTS

linha1= "##########\n"
linha2= "#........#\n"
linha3= "#..$..+..#\n"
linha4= "#........#\n"
linha5= "##########\n"
grelha=linha1+linha2+linha3+linha4+linha5
try:
    p=sokoban(grelha)
    travel_sol = breadth_first_graph_search_plus(p)
    if travel_sol:
        print('Solução em',len(travel_sol.solution()),'passos')
    else:
        print('No way!')
except Exception as e:
    print(repr(e))