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

    def generate_actions(inicial):
        actions = []
        for position in inicial:
            if position.op == 'Empty' or position.op == 'Storage':
                x, y = map(int, position.args[0].op[1:].split('Y'))
                moves = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
                for move in moves:
                    new_x, new_y = x + moves[move][0], y + moves[move][1]
                    new_position = get_position_value(inicial, new_x, new_y)
                    if new_position.op == 'Empty' or new_position.op == 'Storage':
                        actions.append(move_sokoban(new_position.op, x, y, new_x, new_y,))

                        sokoban_x, sokoban_y = sokoban_box_move(move, x, y)
                        sokoban = get_position_value(inicial, sokoban_x, sokoban_y)
                        if valid_box_move(inicial, new_x, new_y, sokoban):
                            actions.append(move_box(x, y, new_x, new_y, sokoban_x, sokoban_y))
        return actions

    def valid_box_move(inicial, x, y, sokoban):
        if sokoban.op != 'Wall':
            if (not empty_puzzle_limit(inicial, x, y)
                    and not empty_corner(inicial, x, y)):
                return True
        return False

    def move_box(x, y, new_x, new_y, sokoban_x, sokoban_y):
        name = expr(f'MoveBox(X{x}Y{y}, X{new_x}Y{new_y})')
        precond = [expr(f'Box(X{x}Y{y})'), expr(f'NotBox(X{new_x}Y{new_y})'),
                   expr(f'Sokoban(X{sokoban_x}Y{sokoban_y})')]
        effect = [expr(f'Box(X{new_x}Y{new_y})'), expr(f'NotBox(X{x}Y{y})'),
                  expr(f'Sokoban(X{x}Y{y})'), expr(f'NotSokoban(X{sokoban_x}Y{sokoban_y})')]
        return Action(name, precond, effect)

    def move_sokoban(position, x, y, new_x, new_y,):
        name = expr(f'MoveSokoban(X{x}Y{y}, X{new_x}Y{new_y})')
        precond = [expr(f'Sokoban(X{x}Y{y})'), expr(f'{position}(X{new_x}Y{new_y})'),
                   expr(f'NotBox(X{new_x}Y{new_y})')]
        effect = [expr(f'NotSokoban(X{x}Y{y})'), expr(f'Sokoban(X{new_x}Y{new_y})')]
        return Action(name, precond, effect)

    puzzle = puzzle.split('\n')
    inicial = process_puzzle(puzzle)
    goals = set_goals(inicial)
    planning = PlanningProblem(inicial, goals, [], [])

    forward_plan = ForwardPlan(planning)
    forward_plan.expanded_actions = generate_actions(inicial)

    return forward_plan


# ____________________________________________________________________
# AUXILIAR FUNCTIONS

def empty_corner(inicial, x, y):
    position = get_position_value(inicial, x, y)
    directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    walls = []
    for new_x, new_y in directions:
        neighbour = get_position_value(inicial, new_x, new_y)
        if neighbour.op == 'Wall':
            walls.append((new_x, new_y))
    if position.op == 'Empty':
        if len(walls) == 2:
            return (walls[0][0] != walls[1][0] and walls[0][1] != walls[1][1])
        if len(walls) > 2:
            return True
    return False


def empty_puzzle_limit(inicial, x, y):
    max_x, max_y = map(int, inicial[-1].args[0].op[1:].split('Y'))
    if x == 1 or x == max_x - 1:
        count = 0
        for k in range(1, max_y):
            count += count_storages(inicial, x, k)
        return count == 0
    elif y == 1 or y == max_y - 1:
        count = 0
        for k in range(1, max_x):
            count += count_storages(inicial, k, y)
        return count == 0
    return False


def count_storages(inicial, x, y):
    count = 0
    for position in inicial:
        if position.args[0].op == f'X{x}Y{y}' and position.op == 'Storage':
            count += 1
    return count


def get_position_value(inicial, x, y):
    for position in inicial:
        if position.op == 'Empty' or position.op == 'Storage' or position.op == 'Wall':
            if position.args[0].op == f'X{x}Y{y}':
                return position


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
