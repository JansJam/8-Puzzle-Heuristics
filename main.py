import copy
import itertools

from datetime import datetime


class Path:

    def __init__(self, state, moves, weight):
        self.state = state
        self.moves = moves  # stores moves to solution
        self.weight = weight  # stores weight of previous moves PLUS heuristic value

    # getters
    def get_state(self):
        return self.state

    def get_moves(self):
        return self.moves

    def get_weight(self):
        return self.weight

    def get_total_heuristic(self, ):
        return self.weight + get_heuristic(self.state, end_puzzle)

    # setters
    def set_state(self, state):
        self.state = state

    def add_moves(self, move):
        self.moves.append(move)
        self.weight = len(self.moves)

    def switch_block(self, row, j, new_i, new_j):
        temp = self.state[row][j]
        self.state[row][j] = self.state[new_i][new_j]
        self.state[new_i][new_j] = temp


def get_manhattan(current_state, goal_state):
    manhattan_distance = 0
    for i, j in itertools.product(range(3), range(3)):  # Iterate through start state
        for x, y in itertools.product(range(3), range(3)):  # Iterate through end state
            if current_state[i][j] == "0":  # Ignores distance between empty blocks (i.e. 0)
                break
            if current_state[i][j] == goal_state[x][y]:
                # Adds the distance between vertical row and horizontal row
                manhattan_distance += abs(i - x) + abs(j - y)
                break

    return manhattan_distance


def misplaced_tiles(current_state, goal_state):
    misplaced_tiles = 0
    for i, j in itertools.product(range(3), range(3)):  # Iterate through start state
        if current_state[i][j] != goal_state[i][j]:
            misplaced_tiles += 1

    return misplaced_tiles


def swap(path):
    for i, j in itertools.product(range(3), range(3)):  # Finding the empty block (Linear search)

        if path.get_state()[i][j] == 0:

            new_paths = []

            if i > 0:
                up_path = copy.deepcopy(path)
                up_path.switch_block(i, j, i - 1, j)
                up_path.add_moves('U')
                new_paths.append(up_path)

            if j > 0:
                left_path = copy.deepcopy(path)
                left_path.switch_block(i, j, i, j - 1)
                left_path.add_moves('L')
                new_paths.append(left_path)

            if i < 2:
                down_path = copy.deepcopy(path)
                down_path.switch_block(i, j, i + 1, j)
                down_path.add_moves('D')
                new_paths.append(down_path)

            if j < 2:
                right_path = copy.deepcopy(path)
                right_path.switch_block(i, j, i, j + 1)
                right_path.add_moves('R')
                new_paths.append(right_path)

            return new_paths


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    start_puzzle = [[4, 1, 3], [2, 6, 8], [0, 7, 5]]
    end_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    user_input = input("Please input '1' for Manhattan, or '2' for Misplaced Tiles")

    if user_input == "1":
        get_heuristic = get_manhattan
    elif user_input == "2":
        get_heuristic = misplaced_tiles

    start = Path(start_puzzle, [], 0)

    all_paths = [start]
    start_time = datetime.now()
    while True:
        lowest_path = all_paths[0]
        save = 0
        for index, a in enumerate(all_paths):
            if lowest_path.get_total_heuristic() > a.get_total_heuristic():
                lowest_path = a
                save = index
        all_paths.pop(save)

        if get_heuristic(lowest_path.get_state(), end_puzzle) == 0:
            break

        new = swap(lowest_path)
        for a in new:
            all_paths.append(a)
    print(lowest_path.get_moves())
    print("time taken")
    end_time = datetime.now()
    print(end_time - start_time)
