from board import *

def hill_climbing(board):
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
        print_board(board) 
        print("Solved!")
        print("---  Time: %s sec ---" % (time.time() - start_time))
        return
    else:
        print_board(board)
        print("Could not find optimal solution.")
        print("Points away from optimum: ", optimum - evaluate_state(board))
    print("---  Time: %s sec ---" % (time.time() - start_time))