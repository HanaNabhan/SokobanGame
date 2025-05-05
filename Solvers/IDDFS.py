from collections import deque
import time
from Levels.level import Level
from utils.funcs import *
import copy
 
max_depth = 1000  
possibleMoves = ((0, 1), (1, 0), (0, -1), (-1, 0))
timeLimit = 60
 
def iterativeDeepeningDFS(boardState):
     timeStart = time.time()
     for depth in range(max_depth):
         if time.time() > timeStart + timeLimit:
             print("Time limit of", timeLimit, "secs exceeded")
             return boardState
         solved , lastState = DLS(boardState, depth , timeStart)
         if solved:
             return lastState
     return boardState
         
 
def DLS(boardState , depth , timeStart):
     # print("Starting Depth Limited Search" , depth, "steps")
     stateHist = []
     stack = []
     stack.append((copy.deepcopy(boardState) , depth))
     while stack:
         lastState , curr_depth = stack.pop()
         if curr_depth == 0 and check(lastState) :
             print("Solved in", depth, "steps in time" , time.time()-timeStart, "secs", sep = " ")
             return (True , lastState)
         for step in possibleMoves:
             newState = copy.deepcopy(lastState)
             if isLegal(newState, step) and not blocked(newState, step):
                 move(newState, step)
                 if curr_depth > 0 and not searchHist(newState, stateHist):
                     stack.append((newState , curr_depth - 1))
                     stateHist.append(newState)
     return (False , None)
 