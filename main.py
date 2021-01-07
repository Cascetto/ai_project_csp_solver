from csp_solver import *

if __name__ == '__main__':
    csp = CSP()
    csp.add_variable('x1', ['1..2'])
    csp.add_variable('x2', ['1..2'])
    csp.add_constraint('all-diff')
    bs = BacktrackSolver(csp)
    bs.print()
    print(bs.check_consistency())
    print(bs.solve())
