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
                elif symbol == '@':
                    inicial.append(expr(f'PlayerE(X{row}Y{col})'))
                elif symbol == '$':
                    inicial.append(expr(f'Box(X{row}Y{col})'))
                elif symbol == '+':
                    inicial.append(expr(f'PlayerS(X{row}Y{col})'))
        return inicial

    def get_goal(inicial):
        goals = []
        for clause in inicial:
            if clause.op == 'Storage' or clause.op == 'PlayerS':
                goal = expr(f'Box({clause.args[0]})')
                goals.append(goal)
        return associate('&', goals)

    def expand_all_actions(inicial):
        actions, player = [], None

        for clause in inicial:
            if clause.op == 'PlayerE' or clause.op == 'PlayerS':
                player = clause
        playerX, playerY = map(int, player.args[0].op[1:].split('Y'))

        max_rows, max_cols = 0, 0
        for clause in inicial:
            x, y = map(int, clause.args[0].op[1:].split('Y'))
            max_rows = max(max_rows, x)
            max_cols = max(max_cols, y)
        possible_moves = [(playerX - 1, playerY), (playerX + 1, playerY), (playerX, playerY - 1), (playerX, playerY + 1)]

        for next_row, next_col in possible_moves:
            if 0 < next_row <= max_rows or 0 < next_col <= max_cols:
                next_cell = inicial[next_row * (max_cols + 1) + next_col]

                if next_cell.op == 'Empty':
                    action = Action(expr(f'Move(X{playerX}Y{playerY}, X{next_row}Y{next_col})'),
                                    precond=[expr(f'{player.op}(X{playerX}Y{playerY})')],
                                    effect=[expr(f'Storage(X{playerX}Y{playerY})'), expr(f'PlayerE(X{next_row}Y{next_col})')],
                                    domain=[expr(f'{player.op}(X{playerX}Y{playerY})')])
                    actions.append(action)

        # TODO Handle all possible effects meaning:
        #  When the player moves to a empty position
        #  When the player moves to a store position
        #  When the player moves to a box position

        return actions

    def is_valid_puzzle(inicial):
        # TODO: make sure puzzle is valid before expanding actions
        return True

    puzzle = puzzle.strip().split('\n')
    inicial = process_puzzle(puzzle)
    goal = get_goal(inicial)

    planning = PlanningProblem(inicial, goal, [], [])

    forward_plan = ForwardPlan(planning)
    if is_valid_puzzle(inicial):
        forward_plan.expanded_actions = expand_all_actions(inicial)

    return forward_plan


# ____________________________________________________________________
# TESTS

# Expected: Solução em 9 passos
linha1 = "##########\n"
linha2 = "#........#\n"
linha3 = "#..$..+..#\n"
linha4 = "#........#\n"
linha5 = "##########\n"
grelha = linha1 + linha2 + linha3 + linha4 + linha5
try:
    p = sokoban(grelha)
    travel_sol = breadth_first_graph_search_plus(p, True)
    if travel_sol:
        print('Solução em', len(travel_sol.solution()), 'passos')
    else:
        print('No way!')
except Exception as e:
    print(repr(e))
