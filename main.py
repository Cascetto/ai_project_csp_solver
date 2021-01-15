from csp_solver import *

if __name__ == '__main__':
    csp = CSP_magicsequence(10)
    print(backtrack(csp), csp.count)

