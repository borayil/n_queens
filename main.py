from annealing import *
from hillclimbing import *
from genetic import *


def main():
    
    try:
        nqueens = int(input(f'How many queens? (Between 1 and {MAXQ})\n> '))    
        if nqueens < 1 or nqueens > MAXQ:
            raise ValueError
        if nqueens == 2 or nqueens == 3:
            print(f'\nNote that there is no possible solutions for {nqueens} queens.\n')

    except ValueError:
        print(f"Try between 1 and {MAXQ}")
        return False

    print('Which algorithm to use?')
    algorithm = input('| 1: hill-climbing | 2: simulated annealing | 3: genetic algorithm | \n> ')

    try:
        algorithm = int(algorithm)
        if algorithm not in range(1,5):
            raise ValueError
    except ValueError:
        print('No corresponding algorithm! Try again.')
        return False

    board = init_board(nqueens)
    print('Initial board')
    print_board(board)

    if algorithm == 1:
        hill_climbing(board)
    if algorithm == 2:
        simulated_annealing(board, nqueens)
    if algorithm == 3:
        genetic_algorithm(nqueens)


if __name__ == "__main__":
    main()
