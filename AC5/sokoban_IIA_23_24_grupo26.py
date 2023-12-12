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

import timeit


def sokoban(puzzle):
    def process_puzzle(puzzle):
        inicial = []
        for row, line in enumerate(puzzle):
            for col, symbol in enumerate(line):
                if symbol == '#':
                    inicial.append(expr(f'Wall(X{row}Y{col})'))
                elif symbol == '.':
                    inicial.append(expr(f'Empty(X{row}Y{col})'))
                    inicial.append(expr(f'NotBox(X{row}Y{col})'))
                    inicial.append(expr(f'NotSokoban(X{row}Y{col})'))
                elif symbol == 'o':
                    inicial.append(expr(f'Storage(X{row}Y{col})'))
                    inicial.append(expr(f'NotBox(X{row}Y{col})'))
                    inicial.append(expr(f'NotSokoban(X{row}Y{col})'))
                elif symbol == '$':
                    inicial.append(expr(f'Box(X{row}Y{col})'))
                    inicial.append(expr(f'Empty(X{row}Y{col})'))
                    inicial.append(expr(f'NotSokoban(X{row}Y{col})'))
                elif symbol == '@':
                    inicial.append(expr(f'Sokoban(X{row}Y{col})'))
                    inicial.append(expr(f'Empty(X{row}Y{col})'))
                    inicial.append(expr(f'NotBox(X{row}Y{col})'))
                elif symbol == '+':
                    inicial.append(expr(f'Sokoban(X{row}Y{col})'))
                    inicial.append(expr(f'Storage(X{row}Y{col})'))
                    inicial.append(expr(f'NotBox(X{row}Y{col})'))
                elif symbol == '*':
                    inicial.append(expr(f'Box(X{row}Y{col})'))
                    inicial.append(expr(f'Storage(X{row}Y{col})'))
                    inicial.append(expr(f'NotSokoban(X{row}Y{col})'))
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
            if position.op == 'Empty' or position.op == 'Storage':
                x, y = map(int, position.args[0].op[1:].split('Y'))
                moves = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
                for move in moves:
                    new_x, new_y = x + moves[move][0], y + moves[move][1]
                    new_position = position_values(inicial, new_x, new_y)
                    if position.op == 'Empty' or position.op == 'Storage':
                        for value in new_position:
                            if value.op == 'Empty':
                                name = expr(f'MoveSokoban(X{x}Y{y}, X{new_x}Y{new_y})')
                                precond = [expr(f'Sokoban(X{x}Y{y})'), expr(f'Empty(X{new_x}Y{new_y})'), expr(f'NotBox(X{new_x}Y{new_y})')]
                                effect = [expr(f'NotSokoban(X{x}Y{y})'), expr(f'Sokoban(X{new_x}Y{new_y})')]
                                actions.append(Action(name, precond, effect))

                                # TODO Optimize box moves:
                                #   Don´t push boxs against a wall in a row/col there there are no storage positions
                                sokoban_x, sokoban_y = sokoban_box_move(move, x, y)
                                name = expr(f'MoveBox(X{x}Y{y}, X{new_x}Y{new_y})')
                                precond = [expr(f'Box(X{x}Y{y})'), expr(f'Empty(X{x}Y{y})'), expr(f'NotBox(X{new_x}Y{new_y})'),
                                           expr(f'Empty(X{new_x}Y{new_y})'), expr(f'Sokoban(X{sokoban_x}Y{sokoban_y})')]
                                effect = [expr(f'Box(X{new_x}Y{new_y})'), expr(f'NotBox(X{x}Y{y})'),
                                          expr(f'Sokoban(X{x}Y{y})'), expr(f'NotSokoban(X{sokoban_x}Y{sokoban_y})')]
                                actions.append(Action(name, precond, effect))
                            elif value.op == 'Storage':
                                name = expr(f'MoveSokoban(X{x}Y{y}, X{new_x}Y{new_y})')
                                precond = [expr(f'Sokoban(X{x}Y{y})'), expr(f'Storage(X{new_x}Y{new_y})'), expr(f'NotBox(X{new_x}Y{new_y})')]
                                effect = [expr(f'NotSokoban(X{x}Y{y})'), expr(f'Sokoban(X{new_x}Y{new_y})')]
                                actions.append(Action(name, precond, effect))

                                # TODO Optimize box moves:
                                #   Don´t push boxs against a wall in a row/col there there are no storage positions
                                sokoban_x, sokoban_y = sokoban_box_move(move, x, y)
                                name = expr(f'MoveBox(X{x}Y{y}, X{new_x}Y{new_y})')
                                precond = [expr(f'Box(X{x}Y{y})'), expr(f'Empty(X{x}Y{y})'), expr(f'NotBox(X{new_x}Y{new_y})'),
                                           expr(f'Storage(X{new_x}Y{new_y})'), expr(f'Sokoban(X{sokoban_x}Y{sokoban_y})')]
                                effect = [expr(f'Box(X{new_x}Y{new_y})'), expr(f'NotBox(X{x}Y{y})'),
                                          expr(f'Sokoban(X{x}Y{y})'), expr(f'NotSokoban(X{sokoban_x}Y{sokoban_y})')]
                                actions.append(Action(name, precond, effect))
        return actions

    def position_values(inicial, x, y):
        values = []
        for position in inicial:
            if position.args[0].op == f'X{x}Y{y}':
                values.append(position)
        return values

    def sokoban_box_move(move, x, y):
        new_x, new_y = x, y
        if move == 'Up':
            new_x += 1
        elif move == 'Down':
            new_x -= 1
        elif move == 'Left':
            new_y += 1
        elif move == 'Right':
            new_y -= 1
        return new_x, new_y

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
start_time = timeit.default_timer()
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
stop_time = timeit.default_timer()
print('Time: ', stop_time - start_time)

# Test 2
start_time = timeit.default_timer()
print('Test 2:')
linha1 = "#######\n"
linha2 = "#.....#\n"
linha3 = "#..$..#\n"
linha4 = "#@....#\n"
linha5 = "#o....#\n"
linha6 = "#######\n"
grelha = linha1 + linha2 + linha3 + linha4 + linha5 + linha6
p = sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
    print('Solução em', len(travel_sol.solution()), 'passos')
    print(travel_sol.solution())
else:
    print('No way!')
stop_time = timeit.default_timer()
print('Time: ', stop_time - start_time)

# Test 3
start_time = timeit.default_timer()
print('Test 3:')
linha1 = "#######\n"
linha2 = "#.o...#\n"
linha3 = "#.#...#\n"
linha4 = "#.#.#.#\n"
linha5 = "#..$..#\n"
linha6 = "#..@..#\n"
linha7 = "#######\n"
grelha = linha1 + linha2 + linha3 + linha4 + linha5 + linha6 + linha7
p = sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
    print('Solução em', len(travel_sol.solution()), 'passos')
    print(travel_sol.solution())
else:
    print('No way!')
stop_time = timeit.default_timer()
print('Time: ', stop_time - start_time)

# Test 4
start_time = timeit.default_timer()
print('Test 4:')
linha1 = "#######\n"
linha2 = "#.o...#\n"
linha3 = "#.#.#.#\n"
linha4 = "#.#.#.#\n"
linha5 = "#.$@..#\n"
linha6 = "#.....#\n"
linha7 = "#######\n"
grelha = linha1 + linha2 + linha3 + linha4 + linha5 + linha6 + linha7
p = sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
    print('Solução em', len(travel_sol.solution()), 'passos')
    print(travel_sol.solution())
else:
    print('No way!')
stop_time = timeit.default_timer()
print('Time: ', stop_time - start_time)

# Test 5
stop_time = timeit.default_timer()
print('Test 5:')
linha1= "  ##### \n"
linha2= "###...# \n"
linha3= "#.@$..# \n"
linha4= "###..o# \n"
linha5= "#o##..# \n"
linha6= "#.#...##\n"
linha7= "#$.....#\n"
linha8= "#......#\n"
linha9= "########\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9
p=sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
   print('Solução em',len(travel_sol.solution()),'passos')
   print(travel_sol.solution())
else:
   print('No way!')
stop_time = timeit.default_timer()
print('Time: ', stop_time - start_time)

# Test 6
stop_time = timeit.default_timer()
print('Test 6:')
linha1= "#######\n"
linha2= "#.o..o#\n"
linha3= "#.#.#.#\n"
linha4= "#.#.#.#\n"
linha5= "#.$@..#\n"
linha6= "#.#...#\n"
linha7= "#######\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7
p=sokoban(grelha)
travel_sol = breadth_first_graph_search_plus(p)
if travel_sol:
   print('Solução em',len(travel_sol.solution()),'passos')
else:
   print('No way!')
stop_time = timeit.default_timer()
print('Time: ', stop_time - start_time)