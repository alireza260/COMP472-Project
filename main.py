import numpy as np
import time

print("board size:")
n = int(input())

if n < 3:
    n = 3
    print("board size adjusted to 3")
elif n > 10:
    n = 10
    print("board size adjusted to 10")

og_board = np.random.randint(2, size=(n, n))

print("dfs max depth:")
max_d = int(input())


def print_matrix(matrix):
    for arr in matrix:
        for ele in arr:
            print("{}".format(ele).rjust(3), end="")
        print(end="\n")
    print(end="\n")


def flip(board, row_index, col):
    board_copy = [[tile for tile in row] for row in board]

    board_copy[row_index][col] ^= 1

    if col - 1 >= 0:
        board_copy[row_index][col - 1] ^= 1

    if col + 1 < n:
        board_copy[row_index][col + 1] ^= 1

    if row_index - 1 >= 0:
        board_copy[row_index - 1][col] ^= 1

    if row_index + 1 < n:
        board_copy[row_index + 1][col] ^= 1

    return board_copy


def get_next_tile(row, col):
    if col + 1 >= n:
        row += 1
        col = 0
    else:
        col += 1

    return row, col


def determine_best(old, new):
    if old is None:
        return new

    if new is None:
        return old

    # " the goal is to find the smallest number of moves to bring the board to its goal configuration"
    if old[0] < new[0]:
        return old
    if new[0] < old[0]:
        return new

    # Prefer "the board that has its first white token(s) at an earlier position based on left-to-right, then top-down order"
    for t1, t2 in zip(old[1], new[1]):  # Iterate through each move
        b1 = t1[2]
        b2 = t2[2]

        for arr1, arr2 in zip(b1, b2):  # Iterate through each row
            for ele1, ele2 in zip(arr1, arr2):  # Iterate through each tile
                if ele1 < ele2:
                    return old
                if ele2 < ele1:
                    return new


def recur_dfs(board, row_index, col_index, depth):
    """
    Returns None if no solution was found, or a tuple with:
    - the depth (i.e. number of moves + 1)
    - the solution steps: an array of tuples with: row, col, board matrix
    """
    # Check board bounds and depth
    if row_index >= n or col_index >= n or depth > max_d:  # "max_d is included"
        return None

    new_board = flip(board, row_index, col_index)

    if not any(1 in row for row in new_board):
        return depth, [(row_index, col_index, new_board)]

    best = None

    for r_index, row in enumerate(new_board):
        for c_index, tile in enumerate(row):
            if r_index == row_index and c_index == col_index:
                continue
            new = recur_dfs(new_board, r_index, c_index, depth + 1)
            best = determine_best(best, new)

    if best is None:
        return None

    best[1].append((row_index, col_index, new_board))
    return best


def dfs(board):
    return recur_dfs(board, 0, 0, 1)  # "root = 1"


print_matrix(og_board)  # TODO delete

start = time.time()
result = dfs(og_board)
end = time.time()
print(end - start)

if result is None:
    print("No solution")
else:
    result_depth, result_steps = result
    print(result_depth)
    for i in reversed(result_steps):
        print_matrix(i[2])
