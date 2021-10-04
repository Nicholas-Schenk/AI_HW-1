from colorama import Fore, Back, Style
import timeit

from generate import generate
from astar import forward_astar

GRID_SIZE = 101 - 89
NUM_GRIDS = 50 - 45
#defaults are grid size 101 and 50 grids, smaller numbers are only used for testing purposes!

#generate all grids 
def main():
    start = timeit.default_timer()
    grids = generate()
    stop = timeit.default_timer()
    print('Runtime: ' + str(stop - start) + 'seconds (was ~3 sec for me)')

    print_all_grids(grids)

    #run repeated forward a star
    forward_astar

# print a certain grid, given an index
def print_grid(grids, i):
    print("Grid: " + str(i) + ", Size:[" + str(GRID_SIZE) + ", " + str(GRID_SIZE) + "]\n")
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell = grids[i][x][y]
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

if __name__ == "__main__":
    main()
    