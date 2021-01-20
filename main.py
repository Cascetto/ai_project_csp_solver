from csp_solver import *
from matplotlib import pyplot as plt

if __name__ == '__main__':
    n_of_queens = 8
    n_of_sudoku = 3
    k = 10

    nqueen_sample = None
    nsudoku_sample = None

    # no inference strategy battery test
    # x: test number; y: test counter
    sudoku_data = []
    queen_data = []
    for i in range(k):
        backtrack(s := create_n_sudoku(n_of_sudoku), no_inference)
        backtrack(q := create_n_queen(n_of_queens), no_inference)
        sudoku_data.append(s.explorations)
        queen_data.append(q.explorations)
    plt.xlabel("Test number")
    plt.ylabel("Nodes explored")
    plt.title("Sudoku set")
    plt.plot([i for i in range(1, k + 1)], sudoku_data)
    plt.show()
    plt.title("N-Queen set")
    plt.plot([i for i in range(1, k + 1)], queen_data)
    plt.show()
