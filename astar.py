from BinaryHeap import BinaryHeap
from typing import Counter
from colorama import Fore, Back, Style
#import heapq as hq
import random

from State import State

#implementation of repeated forward A*
def forward_astar(grid, agent_pos, target_pos, size, g_tie_breaker):

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
    EXPANSIONS = 0

    #print_grid(GRID, agent_state, target_state.pos)
    
    while agent_state.pos != target_pos:
        COUNTER = COUNTER + 1
        if COUNTER > 0 and COUNTER%500 == 0: 
            print_grid(GRID, agent_state, target_state.pos)
            print(COUNTER)
            if COUNTER == 5000:
                return [-1, EXPANSIONS]
        agent_state.g_cost = 0
        agent_state.search = COUNTER

        target_state.g_cost = GRID_SIZE**2
        target_state.search = COUNTER

        #open list is a min heap representing list of tuples (primary key, 2ndary key, order of insertion, value) using key to maintain minimum ordering in the heap
        open_list = BinaryHeap()
        closed_list = []
        order = 0   #order is extremely important for breaking ties for heap insertion, without it the program will crash
        heap_insert(agent_state, order, open_list, g_tie_breaker)

        #get shortest path for what the agent observes in its current grid
        EXPANSIONS = determine_path(agent_state, target_state, order, open_list, closed_list, g_tie_breaker, EXPANSIONS)
        if len(open_list.heap) == 0 and manhattan_distance(agent_state.pos, target_state.pos) > 1:
            print("Agent cannot reach the Target")
            return [-1, EXPANSIONS]
        
        #trace path from target to agent
        target_state = filter_path(target_state, agent_state)
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

        #print_grid(GRID, agent_state, target_state.pos)

    #print_grid(GRID, agent_state, target_state.pos)
    return [COUNTER, EXPANSIONS]

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
def determine_path(agent_state, target_state, order, open_list, closed_list, g_tie_breaker, expansions):
    # while g(goal_state) > minimum f value state in the heap
    #print("DETERMINING PATH")
    #print(target_state.g_cost)
    while len(open_list.heap) > 0 and target_state.g_cost > open_list.heap[0][0]:
        state = open_list.pop()[3]
        expansions = expansions + 1
        #mark the minmum f value state as visited
        closed_list.append(state)
        #print("expanding: " + state.to_string())
        actions = get_actions(state, closed_list) 
        #actions represent possible successor states that can be visited following this current state
        for action_state in actions:
            #agent found the target, break out of loop
            if action_state.pos == target_state.pos:
                target_state.prev = state

                return expansions

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
                order = order + 1
                heap_insert(action_state, order, open_list, g_tie_breaker)
                
               
        #for action_state in actions:
            #print("added: " + action_state.to_string())
        #print()

    return expansions

#check the path linked list for shortcuts
def filter_path(source_state, dest_state):
    state_list = []
    current = source_state
    while(current != None):
        state_list.append(current)
        current = current.prev

    for i in range(len(state_list)):
        neighbors = get_actions(state_list[i], [])
        for neighbor in neighbors:
           if neighbor.pos == dest_state.pos:
                state_list = state_list[0:i + 1]
                state_list.append(dest_state)
                state_list[-2].prev = dest_state
                
                return source_state
    return source_state
        
#def backward_determine_path(agent_state, target_state, expansions):
    open_list = []
    open_list2 = []
    closed_list = []
    dummy_var = 0
    #STEP 2: start loop
    while dummy_var==0 or len(open_list) > 0:

        #STEP 3: if we have just started, set cur_state to target_state. Otherwise, set it to the lowest in the heap and remove it from the open list
        if dummy_var != 0:
            cur_state = hq.heappop(open_list)[3]
            open_list2.remove(cur_state)
        else:
            cur_state=target_state

        expansions+=1
        #print("expanded: "+ str(cur_state.pos) + " with f_value: "+ str(cur_state.f_value)+ " with g_cost: "+ str(cur_state.g_cost))

        #STEP 4: put cur into closed list
        closed_list.append(cur_state)

        #STEP 4: find out which neighbors are valid
        neighbors = get_actions2(cur_state, closed_list, open_list2)

        #STEP 6: create states for valid neighbors, insert them into the heap
        for neighbor in neighbors:
            #STEP 7: if we found the agent, we need to determine the shortest path based on the g-costs we have in the grid.
            neighbor.prev = cur_state
            if(neighbor.pos == agent_state.pos):
                print("FOUND IT")
                order = [neighbor]
                while neighbor.prev.pos != target_state.pos: 
                    neighbor = neighbor.prev
                    order.append(neighbor)
                order.append(target_state)
                return order, expansions
            #If #we didn't find the target, we should calculate the neighbors f_value and g_cost and add them to the grid.
            #then we push the node onto the heap
            dummy_var+=1
            current_state = neighbor
            current_state.f_value = get_f_value(target_state.pos, neighbor.pos, agent_state.pos)
            current_state.g_cost = get_g_cost(target_state.pos, neighbor.pos )
            #print("set g_cost of: "+ str(current_state.pos))
            tuple = (current_state.f_value, -1 * current_state.g_cost , dummy_var, current_state)
            hq.heappush(open_list, tuple)
            open_list2.append(current_state)
    print("DIDN'T FIND IT")
    return [], expansions

#implementation of repeated backward A*
#def backward_astar(grid, agent_pos, target_pos, size, g_tie_breaker):

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
    EXPANSIONS = 0

    #print_grid(GRID, agent_state, target_state.pos)
    
    while agent_state.pos != target_pos:
        COUNTER = COUNTER + 1
        agent_state.g_cost = 0
        agent_state.search = COUNTER

        target_state.g_cost = GRID_SIZE**2
        target_state.search = COUNTER

        #open list is a min heap representing list of tuples (primary key, 2ndary key, order of insertion, value) using key to maintain minimum ordering in the heap
        open_list = []
        closed_list = []
        order = 0   #order is extremely important for breaking ties for heap insertion, without it the program will crash
        heap_insert(agent_state, order, open_list, g_tie_breaker)

        #get shortest path for what the agent observes in its current grid
        ordered_list, EXPANSIONS = backward_determine_path(agent_state, target_state, EXPANSIONS)
        if len(ordered_list) == 0:
            print("Agent cannot reach the Target")
            return [-1, -1]
        

        #move the agent
        current = ordered_list[1]
        x, y = agent_state.pos
        GRID[x][y] = 0
        agent_state.pos = current.pos
        agent_state.f_value = get_f_value(agent_state.pos, agent_state.pos, target_pos)
        GRID = set_agent_grid(GRID, grid, agent_state, target_state)

        #print_grid(GRID, agent_state, target_state.pos)


    #print_grid(GRID, agent_state, target_state.pos)
    return [COUNTER, EXPANSIONS]

def backward_determine_path2(agent_state, target_state, order, open_list, closed_list, g_tie_breaker, expansions):
    # while g(agent_state) < minimum f value state in the heap
    while len(open_list.heap) > 0 and agent_state.g_cost > open_list.heap[0][0]:
        state = open_list.pop()[3]
        expansions = expansions + 1
        #mark the minmum f value state as visited
        closed_list.append(state)
        #print("expanding: " + state.to_string())
        actions = get_actions(state, closed_list) 
        #actions represent possible successor states that can be visited following this current state
        for action_state in actions:
            #agent found the target, break out of loop
            if action_state.pos == agent_state.pos:
                agent_state.prev = state
                return expansions

            if action_state.search < COUNTER:
                action_state.g_cost = GRID_SIZE**2
                action_state.search = COUNTER

            agent_action_cost = get_g_cost(target_state.pos, action_state.pos)
            #if action_state.g_cost > state.g_cost + agent_action_cost:
            if action_state.g_cost > target_state.g_cost + agent_action_cost:

                #set updated g cost for next state and pointer back to source state
                action_state.g_cost = target_state.g_cost + agent_action_cost
                action_state.prev = state

                #remove the action from the open list if it currently aready exists
                check_and_remove(action_state, open_list)
                action_state.f_value = get_f_value(agent_state.pos, action_state.pos, target_state.pos)

                #insert the successor state into the open list
                heap_insert(action_state, order, open_list, g_tie_breaker)
                order = order + 1
               
        #for action_state in actions:
            #print("added: " + action_state.to_string())
        #print()

    return expansions
    
def backward_astar2(grid, agent_pos, target_pos, size, g_tie_breaker):

    agent_state = State(agent_pos)
    agent_state.f_value = get_f_value(agent_pos, agent_pos, target_pos)
    target_state = State(target_pos)
    target_state.f_value = get_f_value(agent_pos, target_pos, target_pos)

    global GRID_SIZE
    global GRID
    global COUNTER
    
    GRID_SIZE = size
    GRID = [[0] * GRID_SIZE for i in range(GRID_SIZE)]
    GRID = set_agent_grid(GRID, grid, agent_state, target_state)
    COUNTER = 0
    EXPANSIONS = 0

    #print_grid(GRID, agent_state, target_state.pos)
    
    while agent_state.pos != target_pos:
        COUNTER = COUNTER + 1
        agent_state.g_cost = GRID_SIZE**2
        agent_state.search = COUNTER

        target_state.g_cost = 0
        target_state.search = COUNTER

        #open list is a min heap representing list of tuples (primary key, 2ndary key, order of insertion, value) using key to maintain minimum ordering in the heap
        open_list = BinaryHeap()
        closed_list = []
        order = 0   #order is extremely important for breaking ties for heap insertion, without it the program will crash
        heap_insert(target_state, order, open_list, g_tie_breaker)

        #get shortest path for what the agent observes in its current grid
        EXPANSIONS = backward_determine_path2(agent_state, target_state, order, open_list, closed_list, g_tie_breaker, EXPANSIONS)
        if len(open_list.heap) == 0 and manhattan_distance(agent_state.pos, target_state.pos) > 1:
            print("Agent cannot reach the Target")
            return [-1, EXPANSIONS]
        
        #trace path from target to agent
        target_state = filter_path(target_state, agent_state)
        next_state = agent_state.prev
    
        #move the agent
        x, y = agent_state.pos
        GRID[x][y] = 0
        agent_state.pos = next_state.pos
        agent_state.f_value = get_f_value(agent_state.pos, agent_state.pos, target_pos)
        GRID = set_agent_grid(GRID, grid, agent_state, target_state)

        #print_grid(GRID, agent_state, target_state.pos)

    #print final result
    #print_grid(GRID, agent_state, target_state.pos)
    return [COUNTER, EXPANSIONS]











def adaptive_set_heuristic(agent_state):
    heuristic_grid = [[0] * GRID_SIZE for i in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cur_state = State([i, j])
            heuristic_grid[i][j] = get_g_cost(agent_state.pos, cur_state.pos)
        #print(heuristic_grid[i])
    return heuristic_grid



 #get shortest path for what the agent observes in its current grid
def adaptive_determine_path(agent_state, target_state, order, open_list, closed_list, g_tie_breaker, expansions, heuristic_grid):
    # while g(goal_state) > minimum f value state in the heap
    #print("DETERMINING PATH")
    #print(target_state.g_cost)
    agent_state.g_cost = 0
    while len(open_list.heap) > 0 and target_state.g_cost > open_list.heap[0][0]:
        state = open_list.pop()[3]
        expansions = expansions + 1
        #mark the minmum f value state as visited
        closed_list.append(state)
        #print("expanding: " + state.to_string())
        actions = get_actions(state, closed_list) 
        #actions represent possible successor states that can be visited following this current state
        for action_state in actions:
            #agent found the target, break out of loop
            if action_state.pos == target_state.pos:
                target_state.prev = state
                action_state.g_cost = state.g_cost + 1

                #UPDATE HEURISTICS
                #print("TARGET HAS G_COST OF: "+ str(action_state.g_cost))
                for i in closed_list:
                    heuristic_grid[i.pos[0]][i.pos[1]] = action_state.g_cost - i.g_cost 
                #for i in heuristic_grid:
                #    print(i)          
                #print("------------------------------")       


                return expansions

            if action_state.search < COUNTER:
                action_state.g_cost = GRID_SIZE**2
                action_state.search = COUNTER

            agent_action_cost = get_g_cost(state.pos, action_state.pos)
            if action_state.g_cost > state.g_cost + agent_action_cost:
                
                #set updated g cost for next state and pointer back to source state
                action_state.g_cost = state.g_cost + agent_action_cost
                action_state.prev = state
                #print("G COST: "+ str(action_state.g_cost))

                #remove the action from the open list if it currently aready exists
                check_and_remove(action_state, open_list)
                #print("f-value: "+ str(heuristic_grid[action_state.pos[0]][action_state.pos[1]] + action_state.g_cost))
                action_state.f_value = heuristic_grid[action_state.pos[0]][action_state.pos[1]] + action_state.g_cost

                #insert the successor state into the open list
                order = order + 1
                heap_insert(action_state, order, open_list, g_tie_breaker)
                
               
        #for action_state in actions:
            #print("added: " + action_state.to_string())
        #print()


    return expansions







def adaptive_astar(grid, agent_pos, target_pos, size, g_tie_breaker):
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
    EXPANSIONS = 0

    heuristic_grid = adaptive_set_heuristic(target_state)

    #print_grid(GRID, agent_state, target_state.pos)
    
    while agent_state.pos != target_pos:
        COUNTER = COUNTER + 1
        agent_state.g_cost = 0
        agent_state.search = COUNTER

        target_state.g_cost = GRID_SIZE**2
        target_state.search = COUNTER

        #open list is a min heap representing list of tuples (primary key, 2ndary key, order of insertion, value) using key to maintain minimum ordering in the heap
        open_list = BinaryHeap()
        closed_list = []
        order = 0   #order is extremely important for breaking ties for heap insertion, without it the program will crash
        heap_insert(agent_state, order, open_list, g_tie_breaker)

        #get shortest path for what the agent observes in its current grid
        EXPANSIONS = adaptive_determine_path(agent_state, target_state, order, open_list, closed_list, g_tie_breaker, EXPANSIONS, heuristic_grid)
        if len(open_list.heap) == 0 and manhattan_distance(agent_state.pos, target_state.pos) > 1:
            print("Agent cannot reach the Target")
            return [-1, EXPANSIONS]
        
        #trace path from target to agent
        target_state = filter_path(target_state, agent_state)
        current = target_state
        while current.prev != agent_state:
            current = current.prev
        current.prev = None

        #move the agent
        x, y = agent_state.pos
        GRID[x][y] = 0
        agent_state.pos = current.pos
        agent_state.f_value = heuristic_grid[agent_state.pos[0]][agent_state.pos[1]] + get_g_cost(agent_state.pos, target_state.pos)
        GRID = set_agent_grid(GRID, grid, agent_state, target_state)

        #print_grid(GRID, agent_state, target_state.pos)

    #print_grid(GRID, agent_state, target_state.pos)
    return [COUNTER, EXPANSIONS]

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

#def get_actions2(state, closed_list, open_list):
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
    if x - 1 >= 0 and GRID[x - 1][y] != 1 and not check_list(up_state, closed_list) and not check_list(up_state, open_list):
        neighbors.append(up_state)
    #check down direction
    if x + 1 < GRID_SIZE and GRID[x + 1][y] != 1 and not check_list(down_state, closed_list) and not check_list(down_state, open_list):
        neighbors.append(down_state)
    #check left direction
    if y - 1 >= 0 and GRID[x][y - 1] != 1 and not check_list(left_state, closed_list) and not check_list(left_state, open_list):
        neighbors.append(left_state)
    #check right direction
    if y + 1 < GRID_SIZE and GRID[x][y + 1] != 1 and not check_list(right_state, closed_list)and not check_list(right_state, open_list):
        neighbors.append(right_state)
    return neighbors

#insert a state into the min heap open_list as a tuple, order of values in the tuple matters for breaking ties
def heap_insert(state, order, open_list, g_tie_breaker):
    # g_tie_breaker value of -1 means higher g costs used to break ties, value of 1 means lower ones are used
    tuple = (state.f_value, state.g_cost * g_tie_breaker, order, state)
    open_list.insert(tuple)
    #hq.heappush(open_list, tuple)

def check_list(action_state, closed_list):
    for state in closed_list:
        if state.pos == action_state.pos: return True
    return False

def check_and_remove(action_state, open_list):
    for tuple in open_list.heap:
        if tuple[3].pos == action_state.pos:
            open_list.heap.remove(tuple)
            open_list.reheap(0)

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
    print("Agent: " + str(agent_state.pos) + ", Target: " + str(target_pos) )

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
            elif cell == '*':
                print(f"{Fore.BLACK}{Back.WHITE}[" + str(cell) + "]" + f"{Style.RESET_ALL}", end="")
            else:
                print(f"{Fore.WHITE}{Back.WHITE}[ ]" + f"{Style.RESET_ALL}", end="")
        print(" " + str(y))


