# Sokoban Game with Search-Based Solvers

This project implements a Sokoban game and uses a variety of classical and intelligent search algorithms to solve game levels automatically.
<p align="center">
  <img src="https://github.com/HanaNabhan/SokobanGame/blob/main/project%20poster.png" width="900"/>
</p>

## Search Algorithms Implemented

All solvers are located in the `solvers` folder. Each one attempts to solve Sokoban puzzles with different strategies:

- **BFS (Breadth-First Search)**
- **DFS (Depth-First Search)**
- **IDDFS (Iterative Deepening DFS)**
- **IDA\*** (Iterative Deepening A-Star)
- **Greedy Best-First Search**
- **A\*** (A-Star Search)
- **MCTS (Monte Carlo Tree Search)** — _**Main focus of our project**_

---

## 🎯 Project Focus

Our main focus is on the **Monte Carlo Tree Search (MCTS)** solver. We studied its behavior and performance in solving Sokoban puzzles compared to classical algorithms. 

<p align="center">
  <img src="https://github.com/HanaNabhan/SokobanGame/blob/main/mct%20poster.png" width="900"/>
</p>


We compared all solvers based on:
- Number of moves to reach the goal
- Time taken to find a solution
- Memory usage (nodes explored)

---

## 📁 Project Structure

```bash
.
├── game/             # Sokoban game environment
├── solvers/          # All AI algorithms for solving
│   ├── bfs.py
│   ├── dfs.py
│   ├── iddfs.py
│   ├── ida.py
│   ├── greedy.py
│   ├── astar.py
│   └── mcts.py       # 🔥 Main solver of interest
├── levels/           # Game levels
└── README.md

```
## 🕹️ How to Run
```
python main.py
```


