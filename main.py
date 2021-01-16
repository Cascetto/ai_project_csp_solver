from csp_solver import *

if __name__ == '__main__':
    csp = create_n_queen(8)
    print(backtrack(csp), csp.count)

