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
    """
    Creates a ForwardPlan instance for the Sokoban problem.

    Parameters:
    - puzzle: A string representing the Sokoban puzzle.

    Returns:
    - forward_plan: A ForwardPlan instance.
    """
    def process_puzzle(puzzle):
        """
        Process the puzzle string and extract initial state and goals.

        Returns:
        - initial_state: List of Expr representing the initial state.
        - goals: List of Expr representing the goals.
        """
        lines = puzzle.strip().split('\n')
        initial_state = []
        goals = []
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '#':
                    # Wall
                    initial_state.append(Expr('Wall', row, col))
                elif char == '.':
                    # Empty location
                    initial_state.append(Expr('Empty', row, col))
                elif char == 'o':
                    # Storage location
                    goals.append(Expr('Storage', row, col))
                elif char == '@':
                    # Sokoban player
                    initial_state.append(Expr('Player', row, col))
                elif char == '$':
                    # Box
                    initial_state.append(Expr('Box', row, col))
                elif char == '+':
                    # Sokoban player on storage
                    initial_state.append(Expr('Player', row, col))
                    goals.append(Expr('Storage', row, col))
        return initial_state, goals

    # Process the puzzle string
    initial_state, goals = process_puzzle(puzzle)

    planning = PlanningProblem(initial_state, goals, [], [])

    # Create a ForwardPlan instance
    forward_plan = ForwardPlan(planning)

    return forward_plan


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