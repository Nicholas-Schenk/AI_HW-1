from colorama import Fore, Back, Style
import timeit
import heapq as hq

from generate import generate
from astar import forward_astar, backward_astar2, adaptive_astar
from State import State

#generate all grids 
def main():
    start = timeit.default_timer()

    grids = generate(0)
    #grids = generate('Ex')
    #grids = generate('10x10')
    #note: grids are defined in 3D. 1st dimension is NUM_GRIDS, 2nd and 3rd are row and coloumn coordinates respectively

    global GRID_SIZE 
    global NUM_GRIDS 
    GRID_SIZE = len(grids[0])
    NUM_GRIDS= len(grids)

    stop = timeit.default_timer()
    print('Grid Generation Runtime: ' + str(round(stop - start, 5)) + " seconds")

    reports = []

    #run repeated forward A* on all grids
    adaptive_list = []
    forward_list = []
    backward_list = []
    num = 0
    for grid in grids:
        #note: positions are stored in row-column ordered coordinates
        agent_pos, target_pos = get_position('A', grid), get_position('T', grid)
        
        #print_grid(grid, num)
        adaptive_list.append(adaptive_astar(grid, agent_pos, target_pos, GRID_SIZE, -1))
        forward_list.append(forward_astar(grid, agent_pos, target_pos, GRID_SIZE, 1))
        #reports.append(run_adaptive_astar(grid, agent_pos, target_pos, -1))
        #reports.append(run_forward_astar(grid, agent_pos, target_pos, -1))
        #forward_list.append(run_forward_astar(grid, agent_pos, target_pos, 1))
        backward_list.append(backward_astar2(grid, agent_pos, target_pos, GRID_SIZE, -1))

        #report_all_results(reports)
        #reports.clear()
        num+=1
        print("Grid "+ str(num)+ " done")
    adaptive_total = 0
    forward_total = 0
    backward_total = 0
    for i in adaptive_list:
        adaptive_total+=i[1]
    for i in forward_list:
        forward_total += i[1]
    for i in backward_list:
        if type(i[1]) == str:
            print(i[1])
            continue
        backward_total += i[1]
    print("Adaptive Average: "+ str(adaptive_total/NUM_GRIDS))
    print("Forward Average (lower G values): "+ str(forward_total/NUM_GRIDS))
    print("Backward Average: "+ str(backward_total/NUM_GRIDS))


def report_all_results(reports):
    for report in reports:
        print(report)
    print()

def run_and_report(astar, params):
    start = timeit.default_timer()
    results = astar(params[0], params[1], params[2], params[3], params[4])
    stop = timeit.default_timer()
    results.append(round(stop - start, 4))

    if results[0] == -1 or results[1] == -1:
        return params[5][0][0:-25] + "\tFAILED with " + str(results[1]) + " expansions in "+ str(results[2]) + params[5][3]

    return params[5][0]+ str(results[0]) + params[5][1] + str(results[1]) + params[5][2] + str(results[2]) + params[5][3]

def run_forward_astar(grid, agent_pos, target_pos, g_tie_breaker):
    report_statement = ""
    if(g_tie_breaker == -1):
        report_statement = ["Repeated Forward A* Higher G values:\tAgent reached Target in ", " steps, with ",  " expansions in: ", " seconds"]
    else:
        report_statement = ["Repeated Forward A* Lower G values:\tAgent reached Target in ", " steps, with ",  " expansions in: ", " seconds"]
    params = (grid, agent_pos, target_pos, GRID_SIZE, g_tie_breaker, report_statement)
    return run_and_report(forward_astar, params)

def run_backward_astar(grid, agent_pos, target_pos, g_tie_breaker):
    report_statement = ""
    if(g_tie_breaker == -1):
        report_statement = ["Repeated Backward A* Higher G values:\tAgent reached Target in ", " steps, with ",  " expansions in: ", " seconds"]
    else:
        report_statement = ["Repeated Backward A* Lower G values:\tAgent reached Target in ", " steps, with ",  " expansions in: ", " seconds"]
    params = (grid, agent_pos, target_pos, GRID_SIZE, g_tie_breaker, report_statement)
    return run_and_report(backward_astar2, params)

def run_adaptive_astar(grid, agent_pos, target_pos, g_tie_breaker):
    report_statement = ""
    if(g_tie_breaker == -1):
        report_statement = ["Repeated Adaptive A* Higher G values:\tAgent reached Target in ", " steps, with ",  " expansions in: ", " seconds"]
    else:
        report_statement = ["Repeated Adaptive A* Lower G values:\tAgent reached Target in ", " steps, with ",  " expansions in: ", " seconds"]
    params = (grid, agent_pos, target_pos, GRID_SIZE, g_tie_breaker, report_statement)
    return run_and_report(adaptive_astar, params)

# print a certain grid, given an index
def print_grid(grid, i):
    print("Grid: " + str(i) + ", Size:[" + str(GRID_SIZE) + ", " + str(GRID_SIZE) + "]")
    print("Agent: " + str(get_position('A', grid)) + ", Target: " + str(get_position('T', grid)) )

    for column in range(GRID_SIZE):
        if 3 - len(str(column)) == 2:
            print(" " + str(column), end=" ")
        elif 3 - len(str(column)) == 1:
            print(str(column), end=" ")
        else: print(str(column), end="")
    print()

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell = grid[y][x]
            if cell == 1: 
                print(f"{Fore.BLACK}{Back.BLACK}[ ]" + f"{Style.RESET_ALL}", end="")
            elif cell == 'A' or cell == 'T':
                print(f"{Fore.BLACK}{Back.WHITE}[" + str(cell) + "]" + f"{Style.RESET_ALL}", end="")
            else:
                print(f"{Fore.WHITE}{Back.WHITE}[ ]" + f"{Style.RESET_ALL}", end="")
        print(" " + str(y))

def print_all_grids(grids):
    num = 0
    for grid in grids:
        print_grid(grid, num)
        num+=1
        for i in range(GRID_SIZE):
            print("---", end="")
        print()

#search a grid for specific character or flag, returns its coordinate
def get_position(char, grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == char:
                return [y, x]
    return [-1, -1]

if __name__ == "__main__":
    main()
    