from random import randint
from copy import deepcopy

MIN_VALUE = 1
MAX_VALUE = 10
NUM_OF_ITERATIONS = 50
SIZE = 3
epsilon = 0.0000000001


# prints matrix
def printMatrix(m):
    for row in m:
        print([item for item in row])


# prints vector
def printVector(v):
    print([float("{:.10f}".format(item)) for item in v])


# creates a new matrix
# assign each value based on the range from MIN_VALUE and MAX_VALUE
def createMatrix(n):
    matrix = []
    for _ in range(n):
        item = []
        for _ in range(n):
            item.append(randint(MIN_VALUE, MAX_VALUE))
        matrix.append(item)
    return matrix


# creates a new vector
# assign each value based on the range from MIN_VALUE and MAX_VALUE
def createVector(n):
    return [randint(MIN_VALUE, MAX_VALUE) for _ in range(n)]


def swapColumns(m: list, i, j):
    matrix = deepcopy(m)
    size = len(matrix)
    for k in range(size):
        for l in range(size):
            if l == i:
                temp = matrix[k][l]
                matrix[k][l] = matrix[k][j]
                matrix[k][j] = temp
    return matrix


def findMaxIndex(lst: list):
    max_value = 0
    index = 0
    for i in range(len(lst)):
        if lst[i] > max_value:
            max_value = lst[i]
            index = i
    return index


# returns True if matrix has a dominant diagonal,
# or we succeeded creating a dominant diagonal - else False
def createDominantDiagonal(m: list):
    # BRUTE FORCE!
    matrix = deepcopy(m)
    for i in range(SIZE):
        for j in range(SIZE):
            if isDominantDiagonal(matrix):
                return matrix
            if i != j:
                matrix = swapRows(m, i, j)
            for k in range(SIZE):
                for l in range(SIZE):
                    if isDominantDiagonal(matrix):
                        return matrix
                    if k != l:
                        matrix = swapColumns(m, k, l)
    return matrix


# returns True if the matrix has a dominant diagonal - else False
def isDominantDiagonal(m: list):
    for i in range(SIZE):
        if (sum(m[i]) - m[i][i]) > m[i][i]:
            return False
    return True


# swap rows i and j in given matrix
def swapRows(m: list, i: int, j: int):
    matrix = deepcopy(m)
    temp = matrix[i]
    matrix[i] = matrix[j]
    matrix[j] = temp
    return matrix


# transforms the given matrix into a pivot matrix
# returns the pivoted matrix
def pivotMatrix(m: list):
    for i in range(SIZE):
        max_value = 0
        index = 0
        for j in range(i, SIZE):
            if m[j][i] > max_value:
                max_value = m[j][i]
                index = j
        if index != i:
            m = swapRows(m, index, i)
    return m


# isolate the variable and returns the solution
# e.g: 4x +3y = 5 --> x = (5-3y) / 4
def getValue(variable: int, lst: list, sol: int, values: list):
    for i in range(len(lst)):
        sol -= (lst[i] * values[i])
    sol /= variable
    return sol


# returns the current list of values from the iteration
def solveJacobiEquation(m: list, vector: list, temp_values):
    values = deepcopy(temp_values)
    printVector(values)
    for i in range(SIZE):
        if i < SIZE - 1:
            values[i] = getValue(m[i][i],
                                 m[i][:i] + m[i][i + 1:],
                                 vector[i],
                                 temp_values[:i] + temp_values[i + 1:])
        else:
            values[i] = getValue(m[i][i],
                                 m[i][:i],
                                 vector[i],
                                 temp_values[:i])
    return values


# recieves a matrix and a solutions vector - solves the equation using Yaakobi Method
# returns the values based on the stop condition
# stop condition => x(r+1) - x(r) < epsilon
# we declared epsilon in the start of the file
def yaakobiMethod(m: list, vector: list):
    global NUM_OF_ITERATIONS
    temp_values = [0 for _ in range(SIZE)]
    values = solveJacobiEquation(m, vector, temp_values)

    while abs(values[0] - temp_values[0]) > epsilon:
        temp_values = deepcopy(values)
        values = solveJacobiEquation(m, vector, temp_values)
        if NUM_OF_ITERATIONS == 0:
            raise TimeoutError()
        NUM_OF_ITERATIONS -= 1
    return values


# returns the current list of values from the iteration
def solveGausSeidelEquation(m: list, vector: list, temp_values):
    values = deepcopy(temp_values)
    printVector(values)
    for i in range(SIZE):
        if i < SIZE - 1:
            values[i] = getValue(m[i][i],
                                 m[i][:i] + m[i][i + 1:],
                                 vector[i],
                                 values[:i] + values[i + 1:])
        else:
            values[i] = getValue(m[i][i],
                                 m[i][:i],
                                 vector[i],
                                 values[:i])
    return values


# recieves a matrix and a solutions vector - solves the equation using Gaus Seidel Method
# returns the values based on the stop condition
# stop condition => x(r+1) - x(r) < epsilon
# we declared epsilon in the start of the file
def gausSeidelMethod(m: list, vector: list):
    global NUM_OF_ITERATIONS
    temp_values = [0 for _ in range(SIZE)]
    values = solveGausSeidelEquation(m, vector, temp_values)

    while abs(values[0] - temp_values[0]) > epsilon:
        temp_values = deepcopy(values)
        values = solveGausSeidelEquation(m, vector, temp_values)
        if NUM_OF_ITERATIONS == 0:
            raise TimeoutError()
        NUM_OF_ITERATIONS -= 1
    return values


def main():
    # you can choose any size for the matrix and solutions vector
    A = createMatrix(SIZE)
    solution_vector = createVector(SIZE)

    # we start with assigning zeros to the initial values
    values = [0 for _ in range(SIZE)]

    # printing the variables
    print("A:")
    printMatrix(A)
    print(f"\nSolutions vector:\n{solution_vector}")
    print(f"\nStarting values: {values}\n")
    print("Choose method to solve the equation:\n1) Yaakobi\n2) GausSeidel\n"
          "press 1 or 2: ")
    option = int(input())
    if option == 1:
        print("\nYaakobi Method.")
        selected_method = yaakobiMethod
    else:
        print("\nGaus Seidel Method.")
        selected_method = gausSeidelMethod

    # initial checks - pivoting and dominant diagonal
    # first, we pivot the matrix
    A = pivotMatrix(A)

    # next, we check for a dominant diagonal
    # if there isn't one, we try to create one
    # if we cannot create a dominant diagonal,
    # we can still run the system on our matrix and see if it consolidates,
    # if it is, we print the result - else we print an error message
    if not isDominantDiagonal(A):
        A = createDominantDiagonal(A)
        if not isDominantDiagonal(A):
            print("dominant diagonal could not be created!\nTrying to solve the equation without dominant diagonal..\n")
            try:
                values = selected_method(A, solution_vector)
            except TimeoutError:
                print("\u001b[31m" + "VALUES DO NOT CONSOLIDATE! EXITING...")
                exit(0)
            print("even though there is no dominant diagonal, the matrix consolidates!"
                  f"\nvalues:")
            printVector(values)

    else:
        print("Dominant diagonal exists!\nThe result values are:\n")
        values = selected_method(A, solution_vector)
        print("\u001b[32m" + "\nThe final result: ")
        printVector(values)


if __name__ == '__main__':
    main()
