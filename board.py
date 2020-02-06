import numpy as np

closed_list = []
open_list = []

print("board size:")
boardSize = int(input())

if boardSize<3:
    boardSize=3
    print("board size adjusted to 3")
elif boardSize>10:
    boardSize=10
    print("board size adjusted to 10")

random_matrix_array = np.random.randint(2,size=(boardSize,boardSize))


def print_array(random_matrix_array):

    for a in random_matrix_array:
        for elem in a:
            print("{}".format(elem).rjust(3), end="")
        print(end="\n")


def adjacent_nodes(y, x):

    adjacency_list = []

    if x - 1 >= 0:
        adjacency_list.append((y, x-1))

    if x + 1 <= boardSize-1:
        adjacency_list.append((y, x+1))

    if y - 1 >= 0:
        adjacency_list.append((y-1, x))

    if y + 1 <= boardSize-1:
        adjacency_list.append((y+1, x))

    return adjacency_list

def closed_cells(y,x):

    closed_list.append((y,x)) if (y,x) not in closed_list else closed_list

    return closed_list


print_array(random_matrix_array)

number_of_cells = boardSize*boardSize

def open_cells(adjacency_list):

    open_list = [x for x in adjacency_list if x not in closed_list]

    return open_list


def flip_cell(y, x):

    random_matrix_array[y,x] -=1

    if y + 1 <= boardSize-1:
        random_matrix_array[y+1, x] -= 1

    if y - 1 >= 0:
        random_matrix_array[y-1, x] -= 1

    if x + 1 <= boardSize-1:
        random_matrix_array[y, x+1] -= 1

    if x - 1 >= 0:
        random_matrix_array[y, x-1] -= 1

    random_matrix_array[random_matrix_array < 0] = 1

    print_array(random_matrix_array)

def dfs():

    count_white_cells = 0
    y=0
    x=0

    next_cell_y = 0
    next_cell_x = 0

    while count_white_cells != number_of_cells and open_cells(adjacent_nodes(y, x)) != []:
        print_array("-")

        print("choose y:")
        y = int(input())

        while y < 0 or y > boardSize - 1:
            print("choose y:")
            y = int(input())

        print("choose x:")
        x = int(input())

        while x < 0 or x > boardSize - 1:
            print("choose x:")
            x = int(input())



        flip_cell(next_cell_y,next_cell_x)

        next_cell = [cell[0] for cell in open_cells(adjacent_nodes(y, x))]

        next_cell_y = int(str(next_cell)[1])

        next_cell_x = int(str(next_cell)[4])

        count_white_cells = np.count_nonzero(random_matrix_array)

        print("adjacency cells: ")
        print(adjacent_nodes(y, x))

        print("visited cells: ")
        print(closed_cells(y,x))

        print("available cells: ")
        print(open_cells(adjacent_nodes(y, x)))

        print("white cells ratio: ")
        print(count_white_cells , "/" , number_of_cells)

        print(next_cell)

    if not open_cells(adjacent_nodes(y, x)):
        print("There is no solution.")

    elif count_white_cells == number_of_cells:
        print("Congratulations you have won!")

dfs()

