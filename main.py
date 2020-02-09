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

total_moves_tried = 0


def print_matrix(matrix):
    for arr in matrix:
        for ele in arr:
            print("{}".format(ele).rjust(3), end="")
        print(end="\n")
    print(end="\n")


def flip(board, move_history, row_index, col):
    global total_moves_tried
    total_moves_tried += 1

    # Deep copy matrices
    move_history_copy = [[tile for tile in row] for row in move_history]
    board_copy = [[tile for tile in row] for row in board]

    move_history_copy[row_index][col] = True
    board_copy[row_index][col] ^= 1

    if col - 1 >= 0:
        board_copy[row_index][col - 1] ^= 1

    if col + 1 < n:
        board_copy[row_index][col + 1] ^= 1

    if row_index - 1 >= 0:
        board_copy[row_index - 1][col] ^= 1

    if row_index + 1 < n:
        board_copy[row_index + 1][col] ^= 1

    return board_copy, move_history_copy


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

    # "the goal is to find the smallest number of moves to bring the board to its goal configuration"
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


def recur_dfs(board, move_history, depth):
    """
    Returns None if no solution was found, or a tuple with:
    - the depth (i.e. number of moves + 1)
    - the solution steps: an array of tuples with: row, col, board matrix
    """
    # Check for completion
    if not any(1 in row for row in board):
        return depth, []

    if depth == max_d:  # "max_d is included"
        return None

    best = None

    # Brute force recur to every spot on board
    for row_index in range(n):
        for col_index in range(n):
            # Check move history
            if move_history[row_index][col_index]:
                continue

            new_board, new_move_history = flip(board, move_history, row_index, col_index)

            new = recur_dfs(new_board, new_move_history, depth + 1)

            if new is not None:
                # Add move to solution path
                new[1].append((row_index, col_index, new_board))

            # Determine if this move is better than the other moves so far
            best = determine_best(best, new)

    if best is None:
        return None

    return best


def dfs(board):
    empty_history = [x[:] for x in [[False] * n] * n]
    return recur_dfs(board, empty_history, 1)  # "root = 1"


start = time.time()
result = dfs(og_board)
end = time.time()
print("Seconds elapsed: " + str(end - start))
print("Moves tried: " + str(total_moves_tried))

print_matrix(og_board)

if result is None:
    print("No solution")
else:
    result_depth, result_steps = result
    print("Final depth: " + str(result_depth))
    for i in reversed(result_steps):
        print_matrix(i[2])
