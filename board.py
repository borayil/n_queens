import sys
import random
import time
import math

MAXQ = 100
INF = 10000000

# Checks for conflict between (row, column) and (other_row, other_column)
def in_conflict(column, row, other_column, other_row):
    
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


# Chekcs if queen in (row, column) is in conflict with another
def in_conflict_with_another_queen(row, column, board):
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


# Returns amount of queens who can attack each other s
def count_conflicts(board):
    cnt = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen+1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                cnt += 1

    return cnt


def evaluate_state(board):
    n = len(board)
    #Evaluation function. The max amount of conflict can be 1 + 2 + 3 + 4 + .. + = n(n-1)/2
    #(nquees-1) = (nqueens-1)*nqueens/2.
    return ((n-1)*n)/2 - count_conflicts(board)


# Print board row by row
def print_board(board):
    n = len(board)
    for row in range(n):
        line = ''
        for column in range(n):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


# Initializes a board with randomly placed queens
def init_board(nqueens):
    board = []
    for column in range(nqueens):
        board.append(random.randint(0, nqueens-1))
    return board
