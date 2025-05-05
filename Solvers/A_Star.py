from queue import PriorityQueue
import time
import copy
from utils.funcs import *

class AStarSolver:
    def __init__(self, heuristic_type='manhattan'):

        self.pq = PriorityQueue() 
        self.possibleMoves = ((0, 1), (1, 0), (0, -1), (-1, 0)) 
        self.stateHist = set()
        self.timeLimit = 1000  # max time to solve
        self.heuristic_type = heuristic_type
    
    def calculate_heuristic(self, gameState):
        if self.heuristic_type == 'hungarian':
            return calculate_hungarian_heuristic(gameState)
        else:
            return calculate_manhattan_heuristic(gameState)
    
    def solve(self, gameState):
        
        self.pq = PriorityQueue()
        self.stateHist = set()
        
        
        hx = self.calculate_heuristic(gameState)
        num_steps = 0
        
        
        self.pq.put((hx, id(gameState), gameState))
        
        
        timeStart = time.time()
        while time.time() < timeStart + self.timeLimit:
            if self.pq.empty():
                break
                
            lastState = self.pq.get()[2]
            num_steps += 1
            
            if check(lastState):
                return lastState, num_steps
                
            for step in self.possibleMoves:
                newState = copy.deepcopy(lastState)
                if isLegal(newState, step) and not blocked(newState, step):
                    move(newState, step)
                    if not searchHist(newState, self.stateHist):
                        # Calculate heuristic for new state
                        hx = self.calculate_heuristic(newState)
                        
                        # f(n) = g(n) + h(n) where g(n) is num_steps
                        self.pq.put((hx + num_steps, id(newState), newState))
                        addToHist(newState, self.stateHist)
        
        print("Time limit of", self.timeLimit, "secs exceeded")
        return gameState, num_steps


# For backward compatibility
def aStarManhattan(gameState):
    solver = AStarSolver(heuristic_type='manhattan')
    return solver.solve(gameState)

def aStarHungarian(gameState):
    solver = AStarSolver(heuristic_type='hungarian')
    return solver.solve(gameState)
