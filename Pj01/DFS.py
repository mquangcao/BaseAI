class DFS:
    def __init__(self, init_position, mazes_data):
        self.init_position = init_position
        self.mazes_data = mazes_data
        self.ares_start, self.stones_start, self.gol = self.init()

    def init(self):
        ares_start = {
            "x": self.init_position["Ares"]["x"],
            "y": self.init_position["Ares"]["y"]
        }

        stones_start = [
            {"x": self.init_position[key]["x"], "y": self.init_position[key]["y"]}
            for key in self.init_position if key != "Ares"
        ]

        gol = [
            {"x": x, "y": i}
            for i, row in enumerate(self.mazes_data)
            if (x := row.find("$")) != -1
        ]

        return ares_start, stones_start, gol

    def is_gol(self, pos1, pos2):
        return pos1["x"] == pos2["x"] and pos1["y"] == pos2["y"]

    def is_outside(self, pos):
        return pos["x"] < 0 or pos["x"] >= len(self.mazes_data[0]) or pos["y"] < 0 or pos["y"] >= len(self.mazes_data)

    class Position:
        @staticmethod
        def up(pos):
            return {"x": pos["x"], "y": pos["y"] - 1}

        @staticmethod
        def down(pos):
            return {"x": pos["x"], "y": pos["y"] + 1}

        @staticmethod
        def left(pos):
            return {"x": pos["x"] - 1, "y": pos["y"]}

        @staticmethod
        def right(pos):
            return {"x": pos["x"] + 1, "y": pos["y"]}

    def get_neighbor(self, pos):
        neighbors = []
        for direction in [self.Position.up, self.Position.right, self.Position.down, self.Position.left]:
            next_pos = direction(pos)
            if not self.is_outside(next_pos) and not self.is_block(next_pos):
                next_pos["father"] = pos
                neighbors.append(next_pos)
        return neighbors

    def is_block(self, pos):
        x, y = pos["x"], pos["y"]
        return self.mazes_data[y][x] == "x"

    def hash_obj(self, pos):
        return f"{pos['x']},{pos['y']}"

    def symmetry(self, current, next_pos):
        if current["x"] == next_pos["x"]:
            return {"x": current["x"], "y": 2 * current["y"] - next_pos["y"]}
        if current["y"] == next_pos["y"]:
            return {"x": 2 * current["x"] - next_pos["x"], "y": current["y"]}
        return None

    def ares_find_pos_dfs(self, ares_pos, target_pos, block):
        open_list = [ares_pos]
        close_set = set()

        if self.is_block(target_pos) or self.pos_of_array(target_pos, block):
            return {"result": False, "data": []}

        while open_list:
            current = open_list.pop()
            if self.is_gol(current, target_pos):
                path = [{"x": current["x"], "y": current["y"]}]
                while "father" in current:
                    current = current["father"]
                    path.insert(0, current)
                for e in path:
                    e.pop("father", None)
                return {"result": True, "data": path}

            close_set.add(self.hash_obj(current))
            for next_pos in self.get_neighbor(current):
                if self.hash_obj(next_pos) not in close_set and not self.pos_of_array(next_pos, block):
                    open_list.append(next_pos)

        return {"result": False, "data": None}

    def stone_dfs(self, ares_start, stones_start, gols, index):
        open_list = [stones_start[index]]
        close_set = set()

        while open_list:
            current = open_list.pop()
            for gol_index, gol in enumerate(gols):
                if self.is_gol(current, gol):
                    gols.pop(gol_index)
                    path = [{"x": current["x"], "y": current["y"]}]
                    while "father" in current:
                        current = current["father"]
                        path.insert(0, current)
                    for e in path:
                        e.pop("father", None)
                    return path

            close_set.add(self.hash_obj(current))
            for next_pos in self.get_neighbor(current):
                stones_start[index] = current
                sym = self.symmetry(current, next_pos)
                start = current.get("father", ares_start)
                new_ares_start = {"x": start["x"], "y": start["y"]}
                ares = self.ares_find_pos_dfs(new_ares_start, sym, stones_start)
                if next_pos not in open_list and self.hash_obj(next_pos) not in close_set and ares["result"]:
                    next_pos["Ares"] = ares["data"]
                    open_list.append(next_pos)

        return None

    def run(self):
        paths = []
        start = self.ares_start
        for i in range(len(self.stones_start)):
            path = self.stone_dfs(start, self.stones_start, self.gol, i)
            start = self.stones_start[i]
            paths.append(path)
        return paths

    def pos_of_array(self, pos, arr):
        return any(self.hash_obj(pos) == self.hash_obj(e) for e in arr)


