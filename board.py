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

print_array(random_matrix_array)