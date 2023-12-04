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

    def process_puzzle(puzzle):
        initial_state = []
        for row, line in enumerate(puzzle):
            for col, symbol in enumerate(line):
                if symbol == '#':
                    initial_state.append(expr(f'Wall(R{row},C{col})')) #TESTINGGG
                elif symbol == '.':
                    initial_state.append(expr(f'Empty(R{row},C{col})'))
                elif symbol == 'o':
                    initial_state.append(expr(f'Storage(R{row},C{col})'))
                elif symbol == '@':
                    initial_state.append(expr(f'PlayerE(R{row},C{col})'))
                    initial_state.append(expr(f'Empty(R{row},C{col})'))
                elif symbol == '$':
                    initial_state.append(expr(f'Box(R{row},C{col})'))
                elif symbol == '+':
                    initial_state.append(expr(f'PlayerS(R{row},C{col})'))
                    initial_state.append(expr(f'Storage(R{row},C{col})'))
        return initial_state

    def get_goal(state):
        storages = [] # FIX COPY BUG
        for clause in state:
            if clause.op == 'Storage':
                storages.append(clause)
        for clause in storages:
            clause.op = 'Box'
        return storages

    puzzle = puzzle.strip().split('\n')
    initial_state = process_puzzle(puzzle)
    goal = get_goal(initial_state)
    planning = PlanningProblem(initial_state, goal, [], [])

    forward_plan = ForwardPlan(planning)

    return forward_plan


# ____________________________________________________________________
# TESTS

# Expected: Solução em 9 passos
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