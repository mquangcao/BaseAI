from DFS import DFS
from BFS import BFS

init_position = {
    "Ares": {"x": 4, "y": 1},
    "Stone1": {"x": 2, "y": 3},
    "Stone2": {"x": 4, "y": 2},
}

mazes_data = [
    "xxxxxxxxxxxx",
    "xx$........x",
    "xxxx.......x",
    "x......x...x",
    "x......$...x",
    "xxxxxxxxxxxx",
]

dfs_solver = DFS(init_position, mazes_data)
print(dfs_solver.run())

dfs_solver = BFS(init_position, mazes_data)
print(dfs_solver.run())