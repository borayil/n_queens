import sys
import random
import time
import math

MAXQ = 100
INF = 10000000


def in_conflict(column, row, other_column, other_row):
    """
    Checks if two locations are in conflict with each other.
    :param column: Column of queen 1.
    :param row: Row of queen 1.
    :param other_column: Column of queen 2.
    :param other_row: Row of queen 2.
    :return: True if the queens are in conflict, else False.
    """
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    """
    Checks if the given row and column correspond to a queen that is in conflict with another queen.
    :param row: Row of the queen to be checked.
    :param column: Column of the queen to be checked.
    :param board: Board with all the queens.
    :return: True if the queen is in conflict, else False.
    """
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


def count_conflicts(board):
    """
    Counts the number of queens in conflict with each other.
    :param board: The board with all the queens on it.
    :return: The number of conflicts.
    """
    cnt = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen+1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                cnt += 1

    return cnt


def evaluate_state(board):
    """
    Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    (nquees-1) = (nqueens-1)*nqueens/2. Since we want to do ascending local searches, the evaluation function returns
    (nqueens-1)*nqueens/2 - countConflicts().

    :param board: list/array representation of columns and the row of the queen on that column
    :return: evaluation score
    """
    return (len(board)-1)*len(board)/2 - count_conflicts(board)


def print_board(board):
    """
    Prints the board in a human readable format in the terminal.
    :param board: The board with all the queens.
    """
    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):
    """
    :param nqueens integer for the number of queens on the board
    :returns list/array representation of columns and the row of the queen on that column
    """

    board = []

    for column in range(nqueens):
        board.append(random.randint(0, nqueens-1))

    return board


"""
------------------ Do not change the code above! ------------------
"""

def random_search(board):
    """
    This function is an example and not an efficient solution to the nqueens problem. What it essentially does is flip
    over the board and put all the queens on a random position.
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        if i == 5000:  # Give up after 1000 tries.
            break

        for column, row in enumerate(board):  # For each column, place the queen in a random row
            board[column] = random.randint(0, len(board)-1)

    print('Final State')
    print_board(board)
    if evaluate_state(board) == optimum:
        print('Solved!')
    else:
        print('Could not solve puzzle randomly :(')

    


def hill_climbing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """
    start_time = time.time()
    i = 0
    optimum = (len(board) - 1) * len(board) / 2
    # Main Loop
    # Breaks if:
    # 1. reached iteration limit
    # 2. local maximum reached
    # 3. optimum is reached.

    while evaluate_state(board) != optimum:
        i += 1
        if i == 10000:  # Give up after 1000 tries. (very unreasonable time :D)
            break
        # Bestneighbour starts off as current state
        bestneighbour = board.copy()

        # Loop to find best neighbour state of current
        for column, row in enumerate(board):
            # A neighbour state is a state where a single queen differs in location
            # A queen can either go up or down on a board (unless at edge, while statement checks this)
            upboard = board.copy()   # Possible neighbours where a queen in "column" moves up
            downboard = board.copy() # Possible neighbours where a queen in "column" moves down

            # Move queen downwards and check if state is better or equal
            while downboard[column]+1 < len(board)-1:
                downboard[column] = downboard[column] + 1
                if evaluate_state(downboard) > evaluate_state(bestneighbour):  # Better
                    bestneighbour = downboard.copy()
                if evaluate_state(downboard) == evaluate_state(bestneighbour) and downboard != board: # Equal but different, give it a chance to become best
                    if random.randint(0, 100) > 50:
                        bestneighbour = downboard.copy()

            # Move queen upwards and check if state is better or equal
            while upboard[column] - 1 > 0:
                upboard[column] = upboard[column] - 1
                if evaluate_state(upboard) > evaluate_state(bestneighbour):  # Better
                    bestneighbour = upboard.copy()
                elif evaluate_state(upboard) == evaluate_state(bestneighbour) and upboard != board: # Equal but different, give it a chance to become best
                    if random.randint(0,100) > 50:
                        bestneighbour = upboard.copy()

        # Best neighbour is found after for loop...
        # If lower or equal, random-restart

        # If bestneighbour found is worse than board, break, accepting defeat by local maximum
        if evaluate_state(bestneighbour) <= evaluate_state(board):
            for column, row in enumerate(board):  # For each column, place the queen in a random row
                board[column] = random.randint(0, len(board) - 1)
        else:
            board = bestneighbour.copy()

    # Loop breaked either because
    # 1. reached iteration limit
    # 2. local maximum reached
    # 3. optimum is reached.
    # If optimum was reached, print solution...
    print("Final State")
    if evaluate_state(board) == optimum:
        print("Solved!")
        print_board(board) 
        print("---  Time: %s sec ---" % (time.time() - start_time))
        return
    else:
        print_board(board)
        print("Found local maximum")
        print("Points away from optimum: ", optimum - evaluate_state(board))
    print("---  Time: %s sec ---" % (time.time() - start_time))

# This version I explained in b)...
# This was not good and can not be used with new version implemented
def OLDVERSION_time_to_temperature(t):
    if (t == 1):
        return 100
    bfactor = 0.975 # Very slow decrease / sweet spot
    return (bfactor*time_to_temperature(t-1))

# Cooling schedule / Essential to how annealing works
# factor can be changed based on preference / situtation
# Global Tprev value to keep track of the previous temperature
Tprev = 100
def time_to_temperature(t):
    global Tprev
    # If t==1 (first iteration), start with 100
    if (t == 1):
        return Tprev

    # Change factor between [0.5,0.9] for different results
    # I sticked to 0.75 as a factor
    # 0.9: Very fast cooling
    # 0.7: Middle cooling
    # 0.5 and lower: very slow cooling
    factor = 0.75
    T = Tprev/(1+(factor*Tprev))
    Tprev = T
    return T

def simulated_annealing(board, nqueens):
    # Timer for analysis
    start_time = time.time()
    current = board.copy()

    # Current board and optimum initialization
    optimum = (len(board) - 1) * len(board) / 2

    # A larger board needs to cool down longer...
    # For >= 32, the program tends to take 20 to 50 seconds longer
    # Due to the implementation, T == 0 accounts to 0.000 and on...
    print("Annealing the chess board... Please standby.")
    if nqueens <= 32:
        coolingpoint = 0.0001
    else:
        coolingpoint = 0.00005
        print("That's a lot of queens, please wait at least 45 seconds :) \n(N=64 cools within 42-45 seconds with factor 0.75)")


    for t in range (1,INF):

        # Get temperature for time / iteration
        T = time_to_temperature(t)

        if T < coolingpoint:
            print("Final State")
            if (evaluate_state(current) == optimum):
                print_board(current)
                print("Solved!")
            else:
                print_board(current)
                print("Couldn't find optimal solution...")
                print("Points away from optimum: ", optimum - evaluate_state(current))
            print("---  Time: %s sec ---" % (time.time() - start_time))
            return



        # Random successor of current called "next"
        # Makes sure random is different from current
        next = current.copy()
        while (True):
            next[random.randint(0, len(next)-1)] = random.randint(0, len(next)-1)
            if next != current:
                break

        # DeltaE a.k.a. change in energy
        deltaE = evaluate_state(next) - evaluate_state(current)

        if deltaE > 0:
            #Choose next directly
            current = next.copy()
        else:
            # Choose next with probability of e^(deltaE/temp)
            if random.uniform(0,1) < math.e**(deltaE/T):
                current = next.copy()

def mutation(board):
    chosen = random.randint(0,len(board)-1)
    board[chosen] = random.randint(0, len(board) - 1)
    return

def crossing_over(board1,board2):
    length = len(board1)-1
    chosen = random.randint(0, length)
    for column in range(chosen,length+1):
        swap_variable = board1[column]
        board1[column] = board2[column]
        board2[column] = swap_variable
    return
def copyInto(board1,board2):
    for column in range(0,len(board1)):
        board1[column] = board2[column]
    return
def eval_population(population):
    k = 0
    for i in range(len(population)):
        if(evaluate_state(population[i]) > k):
            k = evaluate_state(population[i])
    return k

def tournament_selection(population):
    i = 0
    while(i+1 < len(population)):
        if(evaluate_state(population[i])> evaluate_state(population[i+1])):
            copyInto(population[i+1],population[i])
        else:
            copyInto(population[i],population[i+1])
        i=i+2
    return

def new_gen(population):
    bestIndex = 0
    worstIndex = 0
    for board in range(len(population)):
        if(evaluate_state(population[board]) > evaluate_state(population[bestIndex])):
            bestIndex = board
        if(evaluate_state(population[board]) < evaluate_state(population[worstIndex])):
            worstIndex = board
    #increasing frequency of good genes
    copyInto(population[worstIndex],population[bestIndex])
    tournament_selection(population)
    crossover1 = random.randint(0,len(population)-1)
    crossover2 = random.randint(0, len(population) - 1)
    while(crossover1 == crossover2):
        crossover2 = random.randint(0, len(population) - 1)
    crossing_over(population[crossover1],population[crossover2])
    mutate1 = random.randint(0,len(population)-1)
    mutate2 = random.randint(0,len(population)-1)
    mutation(population[mutate1])
    mutation(population[mutate2])
    return

def genetic_algorithm(nqueens):
    population = []
    for i in range(10):
        population.append(init_board(nqueens))

    optimum = (nqueens - 1) * nqueens / 2
    iteration = 0
    while(eval_population(population) != optimum):
        new_gen(population)
        iteration += 1
        if(iteration > 10000):
            print("Too many iterations...")
            break
    bestIndex = 0
    for board in range(len(population)):
        if (evaluate_state(population[board]) > evaluate_state(population[bestIndex])):
            bestIndex = board
    print("Final State")
    print_board(population[bestIndex])
    if( evaluate_state(population[bestIndex]) == optimum):
        print("Solved!")
    else:
        print("Could not find optimal solution.")


def main():
    
    try:
        nqueens = int(input('How many queens?\n> '))
        
        if nqueens < 1 or nqueens > MAXQ:
            raise ValueError
        if nqueens == 2 or nqueens == 3:
            print(f'\nNote that there is no possible solutions for {nqueens} queens.\n')

    except ValueError:
        print('Correct Usage: python3 nqueens.py NUMBEROFQUEENS')
        return False

    print('Which algorithm to use?')
    algorithm = input('| 1: random | 2: hill-climbing | 3: simulated annealing | 4: genetic algorithm | \n> ')

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
        random_search(board)
    if algorithm == 2:
        hill_climbing(board)
    if algorithm == 3:
        simulated_annealing(board, nqueens)
    if algorithm == 4:
        genetic_algorithm(nqueens)


# This line is the starting point of the program.
if __name__ == "__main__":
    main()
