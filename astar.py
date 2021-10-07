from os import stat
from colorama import Fore, Back, Style
import heapq as hq

from State import State

#implementation of repeated forward A*
def forward_astar(grid, agent_pos, target_pos, size):
    agent_state = State(agent_pos)
    agent_state.f_value = get_f_value(agent_pos, agent_pos, target_pos)
    target_state = State(target_pos)

    global GRID_SIZE
    global GRID
    global COUNTER
    
    GRID_SIZE = size
    GRID = [[0] * GRID_SIZE for i in range(GRID_SIZE)]
    GRID = set_agent_grid(GRID, grid, agent_state, target_state)
    COUNTER = 0

    print_grid(GRID, agent_state, target_state.pos)
    
    while agent_state.pos != target_pos:
        COUNTER = COUNTER + 1
        agent_state.g_cost = 0
        agent_state.search = COUNTER

        target_state.g_cost = GRID_SIZE**2
        target_state.search = COUNTER

        #open list is a min heap representing list of tuples (key, order of insertion, value) using key to maintain increasing f-values in the heap
        open_list = []
        closed_list = []
        order = 0   #order is extremely important for breaking ties for heap insertion, without it the program will crash
        heap_insert(agent_state, order, open_list)

        #get shortest path for what the agent observes in its current grid
        determine_path(agent_state, target_state, order, open_list, closed_list)
        if len(open_list) == 0:
            print("Agent cannot reach the Target")
            return -1
        
        #trace path from target to agent
        current = target_state
        while current.prev != agent_state:
            current = current.prev
        current.prev = None

        #move the agent
        x, y = agent_state.pos
        GRID[x][y] = 0
        agent_state.pos = current.pos
        agent_state.f_value = get_f_value(agent_state.pos, agent_state.pos, target_pos)
        GRID = set_agent_grid(GRID, grid, agent_state, target_state)

        print_grid(GRID, agent_state, target_state.pos)

    print("Agent reached the Target")  
    return 0

#construct a grid representing what the agent sees at a given step
def set_agent_grid(agent_grid, grid, agent_state, target_state):
    x, y = target_state.pos
    agent_grid[x][y]= 'T'
    x, y = agent_state.pos
    agent_grid[x][y] = 'A'

    #map what agent sees at current step to its previous grid
    if x - 1 >= 0 and grid[x - 1][y] != 'A':
        agent_grid[x - 1][y] = grid[x - 1][y]
    if x + 1 < GRID_SIZE and grid[x + 1][y] != 'A':
        agent_grid[x + 1][y] = grid[x + 1][y]
    if y - 1 >= 0 and grid[x][y - 1] != 'A':
        agent_grid[x][y - 1] = grid[x][y - 1]
    if y + 1 < GRID_SIZE and grid[x][ + 1] != 'A':
        agent_grid[x][y + 1] = grid[x][y + 1]

    return agent_grid

#get shortest path for what the agent observes in its current grid
def determine_path(agent_state, target_state, order, open_list, closed_list):
    # while g(goal_state) > minimum f value state in the heap
    while len(open_list) > 0 and target_state.g_cost > open_list[0][0]:
        state = hq.heappop(open_list)[2]
        #print("expanding: " + str(state.to_string()))
        #mark the minmum f value state as visited
        closed_list.append(state)

        actions = get_actions(state, closed_list) 
        #actions represent possible successor states that can be visited following this current state
        for action_state in actions:
            #agent found the target, break out of loop
            if action_state.pos == target_state.pos:
                target_state.prev = state
                return

            if action_state.search < COUNTER:
                action_state.g_cost = GRID_SIZE**2
                action_state.search = COUNTER

            agent_action_cost = get_g_cost(state.pos, action_state.pos)
            if action_state.g_cost > state.g_cost + agent_action_cost:
                
                #set updated g cost for next state and pointer back to source state
                action_state.g_cost = state.g_cost + agent_action_cost
                action_state.prev = state

                #remove the action from the open list if it currently aready exists
                check_and_remove(action_state, open_list)
                action_state.f_value = get_f_value(agent_state.pos, action_state.pos, target_state.pos)

                #insert the successor state into the open list
                heap_insert(action_state, order, open_list)
                order = order + 1
               
        #for action_state in actions:
            #print("added: " + action_state.to_string())
        print()

#implementation of repeated backward A*
def backward_astar():
    return 0

#checks neighbors of a state for non-blocked states, returns a list of unblocked state tuples
def get_actions(state, closed_list):
    x, y = state.pos
    UP = [x - 1, y]
    up_state = State(UP)
    DOWN = [x + 1, y]
    down_state = State(DOWN)
    LEFT = [x, y - 1]
    left_state = State(LEFT)
    RIGHT = [x, y + 1]
    right_state = State(RIGHT)

    neighbors = []
    #check up direction
    if x - 1 >= 0 and GRID[x - 1][y] != 1 and not check_list(up_state, closed_list):
        neighbors.append(up_state)
    #check down direction
    if x + 1 < GRID_SIZE and GRID[x + 1][y] != 1 and not check_list(down_state, closed_list):
        neighbors.append(down_state)
    #check left direction
    if y - 1 >= 0 and GRID[x][y - 1] != 1 and not check_list(left_state, closed_list):
        neighbors.append(left_state)
    #check right direction
    if y + 1 < GRID_SIZE and GRID[x][y + 1] != 1 and not check_list(right_state, closed_list):
        neighbors.append(right_state)
    return neighbors

#insert a state into the min heap open_list, calculates f-value on insertion
def heap_insert(state, order, open_list):
    tuple = (state.f_value, order, state)
    hq.heappush(open_list, tuple)

def check_list(action_state, closed_list):
    for state in closed_list:
        if state.pos == action_state.pos: return True
    return False

def check_and_remove(action_state, open_list):
    for tuple in open_list:
        if tuple[2].pos == action_state.pos:
            open_list.remove(tuple)


def manhattan_distance(start_pos, end_pos):
    return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])

def get_g_cost(agent_pos, state_pos):
    return manhattan_distance(agent_pos, state_pos)

def get_f_value(agent_pos, state_pos, target_pos):
        # f(s) = g(s) + h(s)
    return get_g_cost(agent_pos, state_pos) + manhattan_distance(state_pos, target_pos)

def print_list(list):
    for (f, o, state) in list:
        print(state.to_string() )

def print_grid(grid, agent_state, target_pos):
    print("Size:[" + str(GRID_SIZE) + ", " + str(GRID_SIZE) + "]")
    print("Agent: " + str(agent_state.pos[::-1]) + ", Target: " + str(target_pos[::-1]) )
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell = grid[y][x]
            if cell == 1: 
                print(f"{Fore.BLACK}{Back.BLACK}[ ]" + f"{Style.RESET_ALL}", end="")
            elif cell == 'A' or cell == 'T':
                print(f"{Fore.BLACK}{Back.WHITE}[" + str(cell) + "]" + f"{Style.RESET_ALL}", end="")
            else:
                print(f"{Fore.WHITE}{Back.WHITE}[ ]" + f"{Style.RESET_ALL}", end="")
        print("")

