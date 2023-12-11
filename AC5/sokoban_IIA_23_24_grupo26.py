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
        inicial = []
        for row, line in enumerate(puzzle):
            for col, symbol in enumerate(line):
                if symbol == '#':
                    inicial.append(expr(f'Wall(X{row}Y{col})'))
                elif symbol == '.':
                    inicial.append(expr(f'Empty(X{row}Y{col})'))
                elif symbol == 'o':
                    inicial.append(expr(f'Storage(X{row}Y{col})'))
                elif symbol == '$':
                    inicial.append(expr(f'Box(X{row}Y{col})'))
                elif symbol == '@':
                    inicial.append(expr(f'Sokoban(X{row}Y{col})'))
                    inicial.append(expr(f'Empty(X{row}Y{col})'))
                elif symbol == '+':
                    inicial.append(expr(f'Sokoban(X{row}Y{col})'))
                    inicial.append(expr(f'Storage(X{row}Y{col})'))
                elif symbol == '*':
                    inicial.append(expr(f'Box(X{row}Y{col})'))
                    inicial.append(expr(f'Storage(X{row}Y{col})'))
        return inicial

    def set_goals(inicial):
        goals = []
        for clause in inicial:
            if clause.op == 'Storage':
                goals.append(expr(f'Box({clause.args[0]})'))
        return goals

    def create_all_actions(inicial):
        actions = []
        for position in inicial:
            if position.op != 'Wall' and position.op != 'BoxOnStorage':
                x, y = map(int, position.args[0].op[1:].split('Y'))
                moves = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
                for move in moves:
                    new_x, new_y = x + moves[move][0], y + moves[move][1]
                    next = get_next_position(inicial, new_x, new_y)
                    if next.op != 'Wall' and next.op != 'BoxOnStorage':
                        # FIXME an action is being generated where sokoban is moving to
                        #  a box position an the box is not being moved
                        if next.op != 'Box':
                            actions.append(Action(expr(f'MoveSokoban(X{x}Y{y}, X{new_x}Y{new_y})'),
                                                  precond=[expr(f'Sokoban(X{x}Y{y})')],
                                                  effect=[expr(f'Sokoban(X{new_x}Y{new_y})'),
                                                          expr(f'NotSokoban(X{x}Y{y})')]))

                        # TODO dont generate actions that moves boxes to coners that aren't storages
                        sokobanX, sokobanY = updateSokoban(move, x, y)
                        actions.append(Action(expr(f'MoveBox(X{x}Y{y}, X{new_x}Y{new_y})'),
                                              precond=[expr(f'Box(X{x}Y{y})'), expr(f'Sokoban(X{sokobanX}Y{sokobanY})')],
                                              effect=[expr(f'Box(X{new_x}Y{new_y})'), expr(f'Sokoban(X{x}Y{y})'),
                                                      expr(f'NotBox(X{x}Y{y})'), expr(f'NotSokoban(X{sokobanX}Y{sokobanY})')]))
        return actions

    def updateSokoban(move, x, y):
        sokobanX, sokobanY = 0, 0
        if move == 'Up':
            sokobanX, sokobanY = x + 1, y
        elif move == 'Down':
            sokobanX, sokobanY = x - 1, y
        elif move == 'Left':
            sokobanX, sokobanY = x, y + 1
        if move == 'Right':
            sokobanX, sokobanY = x, y - 1
        return sokobanX, sokobanY

    def get_next_position(inicial, new_x, new_y):
        for clause in inicial:
            if clause.args[0].op == f'X{new_x}Y{new_y}':
                return clause

    def is_valid_puzzle(inicial):
        # TODO: make sure puzzle is valid before expanding actions
        return True

    puzzle = puzzle.strip().split('\n')
    inicial = process_puzzle(puzzle)
    goals = set_goals(inicial)
    planning = PlanningProblem(inicial, goals, [], [])

    forward_plan = ForwardPlan(planning)
    if is_valid_puzzle(inicial):
        forward_plan.expanded_actions = create_all_actions(inicial)

    return forward_plan


# ____________________________________________________________________
# TESTS

# Test 1
print('Test 1:')
linha1 = "##########\n"
linha2 = "#........#\n"
linha3 = "#..$..+..#\n"
linha4 = "#........#\n"
linha5 = "##########\n"
grelha = linha1 + linha2 + linha3 + linha4 + linha5
p = sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
    print('Solução em', len(travel_sol.solution()), 'passos')
    print(travel_sol.solution())
else:
    print('No way!')

# Test 2
print('Test 2:')
linha1= "#######\n"
linha2= "#.....#\n"
linha3= "#..$..#\n"
linha4= "#@....#\n"
linha5= "#o....#\n"
linha6= "#######\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6
p=sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
    print('Solução em',len(travel_sol.solution()),'passos')
    print(travel_sol.solution())
else:
    print('No way!')

# Test 3
print('Test 3:')
linha1= "#######\n"
linha2= "#.o...#\n"
linha3= "#.#...#\n"
linha4= "#.#.#.#\n"
linha5= "#..$..#\n"
linha6= "#..@..#\n"
linha7= "#######\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7
p=sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
    print('Solução em',len(travel_sol.solution()),'passos')
    print(travel_sol.solution())
else:
    print('No way!')

# Test 4
print('Test 4:')
linha1= "#######\n"
linha2= "#.o...#\n"
linha3= "#.#.#.#\n"
linha4= "#.#.#.#\n"
linha5= "#.$@..#\n"
linha6= "#.....#\n"
linha7= "#######\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7
p=sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
    print('Solução em',len(travel_sol.solution()),'passos')
    print(travel_sol.solution())
else:
    print('No way!')

# Test 5
#print('Test 5:')
#linha1= "  ##### \n"
#linha2= "###...# \n"
#linha3= "#.@$..# \n"
#linha4= "###..o# \n"
#linha5= "#o##..# \n"
#linha6= "#.#...##\n"
#linha7= "#$.....#\n"
#linha8= "#......#\n"
#linha9= "########\n"
#grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9
#p=sokoban(grelha)
#travel_sol = breadth_first_graph_search_plus(p)
#if travel_sol:
#    print('Solução em',len(travel_sol.solution()),'passos')
#else:
#    print('No way!')

# Test 6
#print('Test 6:')
#linha1= "#######\n"
#linha2= "#.o..o#\n"
#linha3= "#.#.#.#\n"
#linha4= "#.#.#.#\n"
#linha5= "#.$@..#\n"
#linha6= "#.#...#\n"
#linha7= "#######\n"
#grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7
#p=sokoban(grelha)
#travel_sol = breadth_first_graph_search_plus(p)
#if travel_sol:
#    print('Solução em',len(travel_sol.solution()),'passos')
#else:
#    print('No way!')