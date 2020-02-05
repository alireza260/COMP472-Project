import numpy as np

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

    if y + 1 <= boardSize-1:
        adjacency_list.append(random_matrix_array[y+1, x])

    if y - 1 >= 0:
        adjacency_list.append(random_matrix_array[y-1, x])

    if x + 1 <= boardSize-1:
        adjacency_list.append(random_matrix_array[y, x+1])

    if x - 1 >=0:
        adjacency_list.append(random_matrix_array[y, x-1])

    return adjacency_list


print_array(random_matrix_array)

print_array("-")


count_white_cells = np.count_nonzero(random_matrix_array)

number_of_cells = boardSize*boardSize


def flip_cell(y, x):

    random_matrix_array[y,x] -=1

    if y + 1 <= boardSize-1:
        random_matrix_array[y+1, x] -= 1

    if y - 1 >= 0:
        random_matrix_array[y-1, x] -= 1

    if x + 1 <= boardSize-1:
        random_matrix_array[y, x+1] -= 1

    if x - 1 >=0:
        random_matrix_array[y, x-1] -= 1

    random_matrix_array[random_matrix_array < 0] = 1

    print_array(random_matrix_array)


while count_white_cells != number_of_cells:

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

    flip_cell(y, x)
else:
    print("Congratulations you have won!")











