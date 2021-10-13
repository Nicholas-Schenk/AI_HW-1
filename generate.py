import random

GRID_SIZE = 101 - 89
NUM_GRIDS = 50 - 45
#defaults are grid size 101 and 50 grids, smaller numbers are only used for testing purposes!

#used for generating random start point
list1 = range(GRID_SIZE)

#used for generating whether or not a box will be blocked
list2 = range(10)

def dfs(grid, x, y, visited, closed, count2):
    # mark node as visited as soon as we visit :)
    visited[x][y] = 1

    #WHAT IS COUNT2?
        #python only allows for around 1000 levels of recursion. I feel like it should be extremely unlikely (0.7^1000, although ig they don't have to be consectuive because backtracking?) that we would exceed that, yet we do constantly?
        # the fact that this line is used so much makes me think there may be some bug i'm not seeing
    count2 +=1
    if(count2 > 950):
        return visited

    #mark the node as visited, then if we roll the dice and it is blocked, bactrack to the previous node
    if random.choice(list2) < 3:
        grid[x][y] = 1 
        return visited

    #options is set up to contain all possible neighbors we have to choose from
    options = []
    if x > 0 and visited[x-1][y] == 0:
        options.append("L")
    if x < GRID_SIZE-1 and visited[x+1][y] == 0:
        options.append("R")
    if y > 0 and visited[x][y-1] == 0:
        options.append("U")
    if y < GRID_SIZE-1 and visited[x][y+1] == 0:
        options.append("D")

    #if options is empty, this level cant do anything anymore. therefore we need to return to the level above and have that node go through its remaining options
    while options != [] :
        direction = random.choice(options)
        if direction == 'L':
            visited = dfs(grid, x-1, y, visited, closed, count2)
        elif direction =='R':
            visited = dfs(grid, x+1, y, visited, closed, count2)
        elif direction == 'U':
            visited = dfs(grid, x, y-1, visited, closed, count2)
        elif direction == 'D':
            visited = dfs(grid, x, y+1, visited, closed, count2)

        #when we eventually get back here, we need to update options to reflect which neighbors are still not visited (and valid of course)
        options = []
        if x > 0 and visited[x-1][y] == 0:
            options.append("L")
        if x < GRID_SIZE-1 and visited[x+1][y] == 0:
            options.append("R")
        if y > 0 and visited[x][y-1] == 0:
            options.append("U")
        if y < GRID_SIZE-1 and visited[x][y+1] == 0:
            options.append("D")
        #print(options)

    #when we reach here, we should have gone through every option this node had, so we close it
        #closing it actually doesnt actually do anything, kinda just symbolic
    closed[x][y] = 1
    return visited

def generate(char):
    #return the example 5x5 grid if exmaple parameter passed in
    if char == 'Ex':
        example_grid = [ [ [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 1, 0], [0, 0, 'A', 1, 'T'] ] ]
        return example_grid

    if char == '10x10':
        example_grid = [ [ [0, 0, 0, 0, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 1, 0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 1, 1, 1], [0, 0, 'A', 1, 0, 0, 0, 0, 0,'T'],
                            [0, 0, 1, 1, 1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ] ]
        return example_grid

    width, height, num_arrs = GRID_SIZE, GRID_SIZE, NUM_GRIDS
    #generate 3D array
    grids = [[[0 for i in range(width)] for j in range(height)] for k in range(num_arrs)] 
    for i in grids:

        visited = [[0 for x in range(width)]  for y in range(height)]
        closed = [[0 for x in range(width)]  for y in range(height)]

        #generate random start position
        start_pos_x = random.choice(list1)
        start_pos_y = random.choice(list1)

        dfs(i, start_pos_x, start_pos_y, visited, closed, 0)

        #check if there are any unvisited nodes and repeat search until there aren't
        while True:
            x = -1
            y = -1
            for j in range(width):
                for k in range(height):
                    if visited[j][k] == 0:
                        x = j
                        y = k
                        break

            if x == -1 and y == -1 :
                break
            else :
                dfs(i, x, y, visited, closed, 0)

        #assign agent start position
        while True:
            if i[start_pos_x][start_pos_y] == 0 and check_neighbors(i, start_pos_x, start_pos_y): 
                i[start_pos_x][start_pos_y] = 'A'
                break
            start_pos_x = random.choice(list1)
            start_pos_y = random.choice(list1)

        #generate random target destination
        while True:
            target_pos_x = random.choice(list1)
            target_pos_y = random.choice(list1)
            if [target_pos_x, target_pos_y] != [start_pos_x, start_pos_y]:
                i[target_pos_x][target_pos_y] = 'T'
                break
        
    return grids

def check_neighbors(grid, x, y):
    if x - 1 >= 0 and grid[x - 1][y] == 0:
        return True
    if x + 1 < GRID_SIZE and grid[x + 1][y] == 0:
        return True
    if y - 1 >= 0 and grid[x][y - 1] == 0:
        return True
    if y + 1 < GRID_SIZE and grid[x][y + 1] == 0:
        return True
    return False
