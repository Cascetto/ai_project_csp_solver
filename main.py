from csp_solver import *

if __name__ == '__main__':
    csp = CSP()
    csp.add_variable('x1', ['1..5'])
    csp.add_variable('x2', ['1..5'])
    csp.add_variable('x3', ['1..5'])
    csp.add_variable('x4', ['1..5'])
    csp.add_variable('x5', ['1..5'])
    csp.add_constraint('all-diff')
    csp.add_constraint('no-diagonal')
    bs = BacktrackSolver(csp)
    bs.print()
    print(bs.solve())
