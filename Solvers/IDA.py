import time
from utils.funcs import *
import copy


class Node:
    def __init__(self, state, g=0, method="manhattan"):
        self.state = state
        self.g = g
        self.h = self.calculate_heuristic(state, method)
    
    def f(self):
        return self.g + self.h
    
    def __lt__(self, other):
        return self.f() < other.f()
    
    def calculate_heuristic(self, state, method):
        if method == "hungarian":
            return calculate_hungarian_heuristic(state)
        else:
            return calculate_manhattan_heuristic(state)


class IDA_Star:
    def __init__(self, heuristic_type='manhattan'):
        self.possibleMoves = ((0, 1), (1, 0), (0, -1), (-1, 0))
        self.timeLimit = 1000  # max time to solve
        self.heuristic_type = heuristic_type
        self.num_steps = 0
        
    def search(self, node, threshold, stateHist):
        f = node.f()
        self.num_steps += 1
        
        if f > threshold:
            return f
            
        if check(node.state):
            return node
            
        minThreshold = float("inf")
        for step in self.possibleMoves:
            newState = copy.deepcopy(node.state)
            if isLegal(newState, step) and not blocked(newState, step):
                move(newState, step)
                if not searchHist(newState, stateHist):
                    newNode = Node(newState, g=node.g + 1, method=self.heuristic_type)
                    addToHist(newNode.state, stateHist)
                    result = self.search(newNode, threshold, stateHist)
                    
                    if isinstance(result, Node):
                        return result
                    if result < minThreshold:
                        minThreshold = result
                        
        return minThreshold
    
    def solve(self, boardState):
        self.num_steps = 0
        timeStart = time.time()
        
        initialNode = Node(boardState, g=0, method=self.heuristic_type)
        threshold = initialNode.f()
        
        while True:
            stateHist = set()
            result = self.search(initialNode, threshold, stateHist)
            
            if time.time() > timeStart + self.timeLimit:
                print("Time limit of", self.timeLimit, "secs exceeded")
                return boardState, self.num_steps
                
            if isinstance(result, Node):
                return result.state, self.num_steps
                
            if result == float("inf"):
                print("No solution")
                return boardState, self.num_steps
                
            threshold = result


def ida_star_manhattan(boardState, heuristic_type='manhattan'):
    solver = IDA_Star(heuristic_type=heuristic_type)
    return solver.solve(boardState)

def ida_star_hungarian(boardState ,  heuristic_type='hungarian'):
    solver = IDA_Star(heuristic_type=heuristic_type)
    return solver.solve(boardState)