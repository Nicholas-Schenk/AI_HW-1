from colorama import Fore, Back, Style
import timeit
import heapq as hq

from generate import generate
from astar import forward_astar
from State import State

#generate all grids 
def main():
    start = timeit.default_timer()

    #grids = generate(0)
    grids = generate('Ex')
    #note: grids are defined in 3D. 1st dimension is NUM_GRIDS, 2nd and 3rd are row and coloumn coordinates respectively

    global GRID_SIZE 
    global NUM_GRIDS 
    GRID_SIZE = len(grids[0])
    NUM_GRIDS= len(grids)

    stop = timeit.default_timer()
    print('Grid Generation Runtime: ' + str(stop - start))

    print_all_grids(grids)

    #run repeated forward A* on all grids
    for grid in grids:
        #note: positions are stored in row-column ordered coordinates
        agent_pos, target_pos = get_position('A', grid), get_position('T', grid)
        
        start = timeit.default_timer()
        forward_astar(grid, agent_pos, target_pos, GRID_SIZE)
        stop = timeit.default_timer()
        print('Forward A* Runtime: ' + str(stop - start))
    
# print a certain grid, given an index
def print_grid(grids, i):
    print("Grid: " + str(i) + ", Size:[" + str(GRID_SIZE) + ", " + str(GRID_SIZE) + "]")
    print("Agent: " + str(get_position('A', grids[i])[::-1]) + ", Target: " + str(get_position('T', grids[i])[::-1]) )
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell = grids[i][y][x]
            if cell == 1: 
                print(f"{Fore.BLACK}{Back.BLACK}[ ]" + f"{Style.RESET_ALL}", end="")
            elif cell == 'A' or cell == 'T':
                print(f"{Fore.BLACK}{Back.WHITE}[" + str(cell) + "]" + f"{Style.RESET_ALL}", end="")
            else:
                print(f"{Fore.WHITE}{Back.WHITE}[ ]" + f"{Style.RESET_ALL}", end="")
        print("")

def print_all_grids(grids):
    for i in range(NUM_GRIDS):
        print_grid(grids, i)
        for x in range(GRID_SIZE):
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
    