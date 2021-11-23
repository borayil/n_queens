from board import *

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
    start_time = time.time()
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
    print("---  Time: %s sec ---" % (time.time() - start_time))