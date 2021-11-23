
from board import *

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