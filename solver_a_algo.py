import builtins
import numpy as np
import time

closed_list = []

def print_matrix(matrix):
    for arr in matrix:
        for ele in arr:
            print("{}".format(ele).rjust(3), end="")
        print(end="\n")
    print(end="\n")


def flatten_matrix(matrix):
    return ''.join(map(str, np.array(matrix).flatten()))


def closed_cells(move):

    closed_list.append(move) if (move) not in closed_list else closed_list

    return closed_list

def flip(board, move_history, row_index, col):
    global total_moves_tried
    total_moves_tried += 1

    states.append(flatten_matrix(board))

    # Deep copy matrices
    move_history_copy = np.matrix.copy(move_history)
    board_copy = np.matrix.copy(board)

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


def recur_a_algo(board, move_history, path_length):
    """
    Returns None if no solution was found, or a tuple with:
    - the path_length (i.e. number of moves + 1)
    - the solution steps: an array of tuples with: row, col, board matrix
    """
    # Check for completion
    if board.sum() == 0:
        return path_length, []

    if path_length == max_d:  # "max_d is included"
        return None

    best = None

    entire_list = []
    open_list = []

    for idx, val in enumerate(board):
        for idy, val in enumerate(board):
            entire_list.append((idx + 1, idy + 1))

    open_list = [x for x in entire_list if x not in closed_list]

    # Brute force recur to every spot in open_list
    for x in open_list:
        # Check move history (making sure flipped cell is not there)
        if move_history[x[0]][x[1]]:
            continue
        # flip each element, getting the row and column value from the list
        new_board, new_move_history = flip(board, move_history, x[0], x[1])
        new = recur_a_algo(new_board, new_move_history, path_length + 1)
        # append the black cell count toi each element in the open_list
        count_bc = np.count_nonzero(new_board)
        x = + (count_bc + path_length)
        # sort open_list according to the 3rd index of each element, which is the appended value
        open_list.sort(key=lambda x: x[2])

        if new is None:
            continue
        # Add move to solution path
        new[1].append((x[0], x[1], new_board))
        # Determine if this move is better than the other moves so far
        best = determine_best(best, new)

    if best is None:
        return None

    return best


def a_algo(board):
    empty_history = np.full((n, n), False)
    return recur_a_algo(board, empty_history, 1)  # "root = 1"


# Start program
print("Enter input file path: ")
input_path = input()
print()

with open(input_path) as input_file:
    for puzzle_index, line in builtins.enumerate(input_file):
        split_line = line.split()
        n, max_d, max_l = map(int, split_line[:-1])

        og_board = np.array(list(split_line[-1])).astype(int).reshape((-1, n))

        states = []
        total_moves_tried = 0

        print("Puzzle:", puzzle_index, " max_d:", max_d)
        print_matrix(og_board)

        start = time.time()
        result = a_algo(og_board)
        end = time.time()

        print("Seconds elapsed:", end - start)
        print("Moves tried:", total_moves_tried)

        with open(str(puzzle_index) + "_a_algo_solution.txt", "w") as a_algo_solution_file:
            if result is None:
                print("no solution")
                a_algo_solution_file.write("no solution")
            else:
                result_path_length, result_moves = result
                print("Final path length:", result_path_length)

                a_algo_solution_file.write("0 " + str(flatten_matrix(og_board)) + "\n")

                for move in reversed(result_moves):
                    r, c, m = move

                    print("closed cells: ", closed_cells((c+1,r+1)))


                    count_black_cells = np.count_nonzero(m)
                    print("black cells remaining: ", count_black_cells)

                    a_algo_solution_file.write(chr(ord('A') + r) + str(c + 1) + " " + str(flatten_matrix(m)) + "\n")
                    print_matrix(m)

        with open(str(puzzle_index) + "_a_algo_search.txt", "w") as a_algo_search_file:
            for state in states:
                a_algo_search_file.write("0 0 0 " + state + "\n")

        print()