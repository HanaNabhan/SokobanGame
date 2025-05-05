import time
import copy
import random
import math
from utils.funcs import *

possibleMoves = ((0, 1), (1, 0), (0, -1), (-1, 0))  # up, right, down, left
timeLimit = 300  

random.seed(42)
global_best_solution = None
global_best_value = float('-inf')

class MCTSNode:
    def __init__(self, gameState, parent=None, action=None, heuristic_type='manhattan'):
        self.gameState = gameState
        self.parent = parent
        self.action = action  
        self.children = []
        self.visits = 0
        self.wins = 0     # accumlated score
        self.untried_actions = list(self.get_legal_actions())
        self.is_terminal = check(gameState)
        self.heuristic_type = heuristic_type  
        self.value = self.calculate_value()
        
    def calculate_value(self): 
        # Calculates and returns a heuristic score for the current game state, with higher values indicating states closer to the goal.

        if self.is_terminal:  # If this is a solution
            return 500
        if self.heuristic_type == 'hungarian':
            return 100 - calculate_hungarian_heuristic(self.gameState)
        else:
            return 100 - calculate_manhattan_heuristic(self.gameState)

    def get_legal_actions(self):
        actions = []
        for move in possibleMoves:
            if isLegal(self.gameState, move) and not blocked(self.gameState, move):
                actions.append(move)
        return actions

    def select_child(self):
    # UCB formula: w/n + c * sqrt(ln(N)/n)
    # where:
    # - w = number of wins (or value)
    # - n = number of visits to the child
    # - N = number of visits to the parent
    # - c = exploration constant (controls exploration vs exploitation balance)
        c = 1.41 
        # If the node is root (no parent), use its own visits; otherwise, use parent’s visit count
        parent_visits = self.visits if self.parent is None else self.parent.visits
        # Sort all children using the UCB1 formula

        s = sorted(self.children, key=lambda child: 
                  (child.wins / (child.visits+1)) + c * math.sqrt(2 * math.log(parent_visits+1) / (child.visits+1)) )
        
        return s[-1]  

    def add_child(self, action): #in expansion step
    # Create a deep copy of the current game state to simulate the action
        child_state = copy.deepcopy(self.gameState)
    # Apply the action to the copied state to get the new state
        move(child_state, action)
    # Create a new MCTSNode with the new state, linking it to the current node as its parent
        child = MCTSNode(child_state, parent=self, action=action)
    # Remove the action from the list of untried actions since it's now being explored
        self.untried_actions.remove(action)
    # Add the new child node to the list of children
        self.children.append(child)
        return child

    def update(self, result): # in backpropagation step
        self.visits += 1 # Increment the visit count (number of times this node has been explored)
        self.wins += result # Add the result of the simulation (e.g., win or loss)
        # self.ressq += result * result  

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def is_leaf(self):
        return len(self.children) == 0


def detect_deadend(gameState):
    for i in range(gameState.rows):
        for j in range(gameState.cols):
            if gameState.matrix[i][j] == 3:  
                
                if gameState.matrix[i][j] == 5:
                    continue
                    
                # Check if box is in a corner
                wall_count = 0
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ny, nx = i + dy, j + dx
                    if (ny < 0 or ny >= gameState.rows or 
                        nx < 0 or nx >= gameState.cols or 
                        gameState.matrix[ny][nx] == 1):  # Wall
                        wall_count += 1
                
                # If two adjacent walls form a corner, it's a deadend
                if wall_count >= 2:
                    horizontal_walls = 0
                    vertical_walls = 0
                    
                    # Check horizontal walls
                    if (i-1 < 0 or gameState.matrix[i-1][j] == 1):
                        horizontal_walls += 1
                    if (i+1 >= gameState.rows or gameState.matrix[i+1][j] == 1):
                        horizontal_walls += 1
                        
                    # Check vertical walls
                    if (j-1 < 0 or gameState.matrix[i][j-1] == 1):
                        vertical_walls += 1
                    if (j+1 >= gameState.cols or gameState.matrix[i][j+1] == 1):
                        vertical_walls += 1
                    
                    # If box is against two perpendicular walls or in a corner
                    if (horizontal_walls >= 1 and vertical_walls >= 1):
                        return True
    return False


def freeze_deadlock(gameState):
    
    for i in range(gameState.rows):
        for j in range(gameState.cols):
            if gameState.matrix[i][j] == 3:  
                
                horizontal_blocked = False
                vertical_blocked = False
                
                # Check horizontal blocking
                if (j-1 < 0 or j+1 >= gameState.cols or 
                    gameState.matrix[i][j-1] == 1 or gameState.matrix[i][j+1] == 1 or
                    gameState.matrix[i][j-1] == 3 or gameState.matrix[i][j+1] == 3):
                    horizontal_blocked = True
                
                # Check vertical blocking
                if (i-1 < 0 or i+1 >= gameState.rows or 
                    gameState.matrix[i-1][j] == 1 or gameState.matrix[i+1][j] == 1 or
                    gameState.matrix[i-1][j] == 3 or gameState.matrix[i+1][j] == 3):
                    vertical_blocked = True
                
                # If box is blocked in both directions and not on a target
                if horizontal_blocked and vertical_blocked:
                    return True
    return False


def mcts_search(gameState, heuristic_type='manhattan'):
    global global_best_solution
    global global_best_value
    
    global_best_solution = None
    global_best_value = float('-inf')
    
    num_steps = 0
    root = MCTSNode(gameState, heuristic_type=heuristic_type)
    
    global_best_solution = copy.deepcopy(gameState)
    global_best_value = root.value
    
    StateHist = set()  # For AC
    
    addToHist(gameState, StateHist)
    
    timeStart = time.time()
    iterations = 0
    
    while time.time() < timeStart + timeLimit:
        iterations += 1
        # 1. Selection
        node = root
        path = []  
        
        while not node.is_terminal and node.is_fully_expanded():
            node = node.select_child()
            path.append(node)
            
            # Check if this state has been visited (AC)
            if searchHist(node.gameState, StateHist):
                # Penalize it
                node.wins -= 50
                break
                

            addToHist(node.gameState, StateHist)
            
            if node.value > global_best_value:
                global_best_solution = copy.deepcopy(node.gameState)
                global_best_value = node.value
                
            if check(node.gameState):
                return node.gameState, num_steps
        
        # 2. Expansion
        if not node.is_terminal and not node.is_fully_expanded():
            action = random.choice(node.untried_actions)
            node = node.add_child(action)
            path.append(node)
            
            # DeadEnd Detections
            if detect_deadend(node.gameState) or freeze_deadlock(node.gameState):
                node.wins -= 100  # Penalize deadends
                continue
                
            addToHist(node.gameState, StateHist)
            
            if node.value > global_best_value:
                global_best_solution = copy.deepcopy(node.gameState)
                global_best_value = node.value
                
            if check(node.gameState):
                return node.gameState, num_steps
        
        # 3. Simulation (Rollout)
        state = copy.deepcopy(node.gameState)
        simulation_visited = set()  # This is different that StateHist ( note )
        
        # Add initial simulation state
        addToHist(state, simulation_visited)

        # rollout
        rollout_depth = 75  # Ay number 
        for _ in range(rollout_depth):
            num_steps += 1
            
            if check(state):
                global_best_solution = copy.deepcopy(state)
                global_best_value = 500  # Maximum value for a solution
                return state, num_steps
                
            legal_moves = []
            for move_dir in possibleMoves:
                if isLegal(state, move_dir) and not blocked(state, move_dir):
                    temp_state = copy.deepcopy(state)
                    move(temp_state, move_dir)
                    # Check for cycles
                    if not searchHist(temp_state, simulation_visited):
                        legal_moves.append(move_dir)
            
            if not legal_moves:
                break  
                
            random_move = random.choice(legal_moves) if legal_moves else None
            if random_move:
                move(state, random_move)
                
                current_value = calculate_state_value(state, heuristic_type)
                if current_value > global_best_value:
                    global_best_solution = copy.deepcopy(state)
                    global_best_value = current_value

                addToHist(state, simulation_visited)  
        
        # 4. Backpropagation
        result = 0
        if check(state): 
            result = 5
        else:
            if heuristic_type == 'hungarian':
                result = calculate_state_value(state, 'hungarian')   
            else:
                result = calculate_state_value(state, 'manhattan')
            result  = 5 * (result / 100)  
            
            # Penalize states with deadends
            if detect_deadend(state) or freeze_deadlock(state):
                result -= 5
        
        for node in path:
            node.update(result)
    if global_best_solution is not None:
        return global_best_solution, num_steps
    
    return gameState, num_steps


def calculate_state_value(state, heuristic_type='manhattan'):
    """Calculate a heuristic value for a given state"""
    if check(state):  
        return 500
    if heuristic_type == 'hungarian':
        return 100-calculate_hungarian_heuristic(state)
    else:
        return 100-calculate_manhattan_heuristic(state)


def mcts_manhattan(gameState):
    return mcts_search(gameState, heuristic_type='manhattan')

def mcts_hungarian(gameState):
    return mcts_search(gameState, heuristic_type='hungarian')

