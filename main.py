from csp_solver import *

if __name__ == '__main__':
    csp = create_n_sudoku(3)
    print_sudoku(3, backtrack(csp))
