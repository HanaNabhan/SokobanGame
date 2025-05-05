def track_complexity(solver_func, state , level):
    from tracemalloc import start , get_traced_memory , stop
    import time
    import os
    import csv
    
    level_num = level+1
    
    # Start measuring time and memory
    start()
    start_time = time.time()
    result, thinking_steps = solver_func(state)
    # print(result.timeLine)
    end_time = time.time()
    time_elapsed = end_time - start_time

    _, peak_memory = get_traced_memory()
    memory_mb = peak_memory / 10**6
    stop()
    
    # Determine heuristic if applicable
    heuristic = "N/A"
    if "manhattan" in solver_func.__name__.lower():
        heuristic = "Manhattan"
    elif "hungarian" in solver_func.__name__.lower():
        heuristic = "Hungarian"
    
    num_steps = len(result.timeLine)
    
    # Create CSV file if it doesn't exist
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "solver_analytics.csv")
    file_exists = os.path.isfile(csv_path)
    
    with open(csv_path, 'a', newline='') as csvfile:
        headers = ["Level", "Solver", "Heuristic", "Time_elapsed", "Memory_MB", "Thinking_steps" , "Solution_steps"]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            "Level": level_num,
            "Solver": solver_func.__name__,
            "Heuristic": heuristic,
            "Time_elapsed": f"{time_elapsed:.4f}",
            "Memory_MB": f"{memory_mb:.2f}",
            "Thinking_steps": thinking_steps,
            "Solution_steps": num_steps,
        })

    print(f"{solver_func.__name__}:")
    print(f"  Time elapsed: {time_elapsed:.4f} seconds")
    print(f"  Peak memory usage: {memory_mb:.2f} MB")
    print(f"  Number of thinking steps: {thinking_steps}")
    print(f"  Number of solution steps: {num_steps}")
    print("-" * 40)


    return result



def printf(obj):
    for i in range(0, len(obj.matrix)):
        for j in range(0, len(obj.matrix[0])):
            if(i == obj.playerY and j == obj.playerX):
                print("@", end = '')
            else:
                print(obj.matrix[i][j], end = '')
        print()
    print("")

def check(currLevel):
    clear = True
    for i in range(0, currLevel.rows):
        for j in range(0, currLevel.cols):
            if currLevel.matrix[i][j] == 2:
                clear = False
    return clear
 
def move(levelObj, vals):
    if levelObj.matrix[levelObj.playerY+vals[1]][levelObj.playerX+vals[0]] == 0 or levelObj.matrix[levelObj.playerY+vals[1]][levelObj.playerX+vals[0]] == 2:
        levelObj.playerY += vals[1]
        levelObj.playerX += vals[0]
        levelObj.timeLine.append(vals)
    else:
        levelObj.matrix[levelObj.playerY+vals[1]][levelObj.playerX+vals[0]] -= 3
        levelObj.matrix[levelObj.playerY+2*vals[1]][levelObj.playerX+2*vals[0]] += 3
        levelObj.playerY += vals[1]
        levelObj.playerX += vals[0]
        levelObj.timeLine.append(vals)

def isLegal(currLevel, vals):
   
    target_y = currLevel.playerY + vals[1]
    target_x = currLevel.playerX + vals[0]
    
    
    if (target_y < 0 or target_y >= currLevel.rows or 
        target_x < 0 or target_x >= currLevel.cols):
        return False
    
    
    if currLevel.matrix[target_y][target_x] == 1:
        return False
        
    
    elif currLevel.matrix[target_y][target_x] == 0 or currLevel.matrix[target_y][target_x] == 2:
        return True
        
    elif currLevel.matrix[target_y][target_x] == 3 or currLevel.matrix[target_y][target_x] == 5:
        # Calculate the position behind the box 
        behind_y = target_y + vals[1]
        behind_x = target_x + vals[0]

        if (behind_y < 0 or behind_y >= currLevel.rows or 
            behind_x < 0 or behind_x >= currLevel.cols):
            return False
            
        if (currLevel.matrix[behind_y][behind_x] != 1 and 
            currLevel.matrix[behind_y][behind_x] != 3 and 
            currLevel.matrix[behind_y][behind_x] != 5):
            return True
            
    # Default case --> move is illegal
    return False

def blocked(currLevel, vals):
    if currLevel.matrix[currLevel.playerY+vals[1]][currLevel.playerX+vals[0]] == 3 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]] != 2:
            if(currLevel.matrix[currLevel.playerY+2*vals[1]+1][currLevel.playerX+2*vals[0]] == 1 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]+1] == 1):
                return True
            elif(currLevel.matrix[currLevel.playerY+2*vals[1]+1][currLevel.playerX+2*vals[0]] == 1 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]-1] == 1):
                return True    
            elif(currLevel.matrix[currLevel.playerY+2*vals[1]-1][currLevel.playerX+2*vals[0]] == 1 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]+1] == 1):
                return True   
            elif(currLevel.matrix[currLevel.playerY+2*vals[1]-1][currLevel.playerX+2*vals[0]] == 1 and currLevel.matrix[currLevel.playerY+2*vals[1]][currLevel.playerX+2*vals[0]-1] == 1):
                return True  
    return False

def searchHist(gameState, hist_set):
    
    matrix_tuple = tuple(tuple(row) for row in gameState.matrix)
    
    player_pos = (gameState.playerY, gameState.playerX)
    
    return (matrix_tuple, player_pos) in hist_set


def addToHist(gameState, hist_set):
    matrix_tuple = tuple(tuple(row) for row in gameState.matrix)
    player_pos = (gameState.playerY, gameState.playerX)
    hist_set.add((matrix_tuple, player_pos))

def moveDictation(moves):
    moveNames = {(1, 0): "Right", (-1, 0): "Left", (0, 1): "Down", (0, -1): "Up"}
    for item in moves:
        print(moveNames[item], end = "=>")

def wallFreeFaces(matrix, pos):
    res = []
    if pos[0] > 0 and matrix[pos[0]-1][pos[1]] not in (1, 6):
        res.append((-1, 0))
    if pos[0] < len(matrix)-1 and (matrix[pos[0]+1][pos[1]]) not in (1, 6):
        res.append((1, 0))
    if pos[1] > 0 and matrix[pos[0]][pos[1]-1] not in (1, 6):
        res.append((0, -1))
    if pos[1] < len(matrix[0])-1 and matrix[pos[0]][pos[1]+1] not in (1, 6):
        res.append((0, 1))
    return res

def manhattanDist(gameState, boxPos):                               #Manhattan distances between all the possible 
    dist = []                                                       #destinations and the current box
    for i in range(0, gameState.rows):
        for j in range(0, gameState.cols):
            if gameState.matrix[i][j] == 2:
                dist.append(abs(boxPos[0]-i)+abs(boxPos[1]-j))
    return dist

def calculate_manhattan_heuristic(gameState):
    """
    Calculate the sum of Manhattan distances from each box to its nearest goal
    """
    total_distance = 0
    box_positions = []
    goal_positions = []
    
    # Collect all box and goal positions
    for i in range(gameState.rows):
        for j in range(gameState.cols):
            if gameState.matrix[i][j] == 3:  # Box
                box_positions.append((i, j))
            elif gameState.matrix[i][j] == 2:  # Goal
                goal_positions.append((i, j))
                
    # For each box, find the minimum distance to a goal
    for box in box_positions:
        min_distance = float('inf')
        for goal in goal_positions:
            distance = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
            min_distance = min(min_distance, distance)
        total_distance += min_distance
        
    return total_distance

def calculate_hungarian_heuristic(gameState):
    from scipy.optimize import linear_sum_assignment
    import numpy as np
    
    box_positions = []
    goal_positions = []
    
    for i in range(gameState.rows):
        for j in range(gameState.cols):
            if gameState.matrix[i][j] == 3:  
                box_positions.append((i, j))
            elif gameState.matrix[i][j] == 2:  
                goal_positions.append((i, j))
    
    if not box_positions or not goal_positions:
        return 0
        
    # Create cost matrix
    cost_matrix = np.zeros((len(box_positions), len(goal_positions)))
    
    for i, box in enumerate(box_positions):
        for j, goal in enumerate(goal_positions):
            cost_matrix[i, j] = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
    
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    total_cost = cost_matrix[row_ind, col_ind].sum()
    
    return total_cost