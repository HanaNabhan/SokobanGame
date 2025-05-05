import time
import copy
from utils.funcs import *

class DFSSolver:
    def __init__(self):
        
        self.stack = []
        self.possibleMoves = ((0, 1), (1, 0), (0, -1), (-1, 0))
        self.stateHist = set()
        self.timeLimit = 1000  # max time to solve
    
    def solve(self, boardState):
        self.stack = []
        self.stateHist = set()
        
        num_steps = 0
        self.stack.append(copy.deepcopy(boardState))
        
        # Start the search with a time limit
        timeStart = time.time()
        while time.time() < timeStart + self.timeLimit:
            if not self.stack:
                break
                
            lastState = self.stack.pop()
            num_steps += 1
            
            if check(lastState):
                return lastState, num_steps
                
            for step in self.possibleMoves:
                newState = copy.deepcopy(lastState)
                if isLegal(newState, step) and not blocked(newState, step):
                    move(newState, step)
                    if not searchHist(newState, self.stateHist):
                        self.stack.append(newState)
                        addToHist(newState, self.stateHist)
        
        print("Time limit of", self.timeLimit, "secs exceeded")
        return boardState, num_steps


def depthFirstSearch(boardState):
    solver = DFSSolver()
    return solver.solve(boardState)
