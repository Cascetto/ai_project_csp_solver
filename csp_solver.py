from random import shuffle
from math import inf, ceil


class CSP:

    def __init__(self):

        self.explorations = 0
        self.domain = dict()
        self.current_domain = dict()
        self.constraint = set()
        self.state = dict()

    def add_variable(self, var_name: str, d: list[str]) -> bool:
        domain = set()
        for element in d:
            if (i := element.find('..')) != -1:
                domain |= {x for x in range(int(element[: i]), int(element[i + 2:]))}
            elif element.isalnum():
                domain |= {int(element)}
            else:
                print("Domain error: " + element)
                return False
        self.domain |= {var_name: domain}
        self.current_domain |= {var_name: domain}
        self.state |= {var_name: None}
        return True

    def add_constraint(self, constraint: str):
        if constraint == "all-different":
            for i in range(length := len(l := list(self.domain.keys()))):
                for j in range(i + 1, length):
                    self.constraint |= {f"{l[i]}!={l[j]}"}
        else:
            self.constraint |= {constraint}

    def complete_assigned(self):
        for val in self.state.values():
            if val is None:
                return False
        return True

    def check_constraint(self, constraint_set: set, temp_assign: dict = None):
        state = temp_assign
        if state is None:
            state = self.state
        for constraint in constraint_set:
            skip = False
            for key in state.keys():
                if (p := constraint.find(key)) != -1:
                    if (p + len(key) + 1 >= len(constraint) or constraint[p: p + len(key) + 1] not in self.state.keys()) and state[key] is None:
                        skip = True
                        break
            if skip:
                continue
            if not eval(constraint, state):
                return False
        return True

    def get_neighbours(self, node) -> set:
        # result = {x: set() for x in self.domain.keys()}
        result = set()
        for constraint in self.constraint:
            if node in constraint:
                for key in (self.domain.keys() - {node}):
                    if (p := constraint.find(key)) != -1 and self.state[key] is None:
                        if p + len(key) + 1 >= len(constraint) or constraint[p: p + len(key) + 1] not in self.domain.keys():
                            result |= {key}
        return result

    def interested_constraints(self, node: str, neighbour: str):
        queue = set()
        for constraint in self.constraint:
            if (p := constraint.find(node)) != -1 and (p2 := constraint.find(neighbour)) != -1:
                if (p + len(node) >= len(constraint) or constraint[p: p + len(node) + 1] not in self.domain.keys()) \
                        and (p2 + len(neighbour) >= len(constraint) or \
                        constraint[p2: p2 + len(neighbour) + 1] not in self.domain.keys()):
                    queue |= {constraint}
        return queue

    def constraints_cardinality(self, key):
        count = 0
        for cons in self.constraint:
            if (p := cons.find(key)) != -1:
                if p + len(key) + 1 >= len(cons) or cons[p: p + len(key) + 1] not in self.domain.keys():
                    count += 1
        return count

    def assign(self, var: str, val: int, removed: dict):
        if val in self.current_domain[var]:
            removed[var] |= (self.current_domain[var] - {val})
            self.current_domain[var] = {val}
            self.state[var] = val

    def unassign(self, var, val):
        self.state[var] = None

    def restore(self, crossouts: dict):
        if crossouts is not False:
            for element in crossouts.keys():
                self.current_domain[element] |= crossouts[element]

    # todo util?
    @staticmethod
    def insert_val(constraint: str, state):
        for key in state.keys():
            constraint = constraint.replace(key, str(state[key]))
        return constraint


def sel_var(csp: CSP):
    minkey = None
    min_cardinality = inf
    min_constraints = -1
    for key in csp.domain.keys():
        if (cardinality := len(csp.current_domain[key])) <= min_cardinality and csp.state[key] is None:
            if cardinality == min_cardinality and csp.constraints_cardinality(key) <= min_constraints:
                continue
            min_cardinality = cardinality
            min_constraints = csp.constraints_cardinality(key)
            minkey = key
    return minkey


def val_order(csp: CSP, var: str):
    scores = []
    for value in csp.current_domain[var]:
        score = 0
        for rvar in csp.current_domain.keys() - {var}:
            for rvalue in csp.current_domain[rvar]:
                if csp.check_constraint(csp.constraint, csp.state | {var: value, rvar: rvalue}):
                    score += 1
        scores.append((value, score))
    scores = sorted(scores, key=lambda x: x[1])
    result = []
    for i in range(len(scores)):
        result.append(scores[i][0])
    return result


def backtrack(csp: CSP, inference):
    if csp.check_constraint(csp.constraint) and csp.complete_assigned():
        return csp.state
    var = sel_var(csp)
    removed = {x: set() for x in csp.domain.keys()}
    for val in val_order(csp, var):
        csp.explorations += 1
        # new node explored
        if csp.check_constraint(csp.constraint, csp.state | {var: val}):
            csp.assign(var, val, removed)
            if inference(csp, var, removed) is not False:
                result = backtrack(csp, inference)
                if result:
                    return result
        csp.restore(removed)
        csp.unassign(var, val)
    return False


def forward_checking(csp: CSP, node: str, removed: dict):
    # queue in form of set of constraints
    # queue = csp.relevant_constraint(node)
    queue = set()
    queue |= {(x, node) for x in csp.get_neighbours(node)}
    while len(queue) > 0:
        arch = queue.pop()
        if _revise(csp, arch, removed) is not False:
            if len(csp.current_domain[node]) == 0:
                return False
    return True


def maintain_arc_consistncy(csp: CSP, node: str, removed: dict):
    # queue in form of set of constraints
    # queue = csp.relevant_constraint(node)
    queue = set()
    queue |= {(x, node) for x in csp.get_neighbours(node)}
    while len(queue) > 0:
        arch = queue.pop()
        if _revise(csp, arch, removed) is not False:
            if len(csp.current_domain[node]) == 0:
                return False
            # mac only
            queue |= {(x, arch[0]) for x in (csp.get_neighbours(arch[0]))}
    return True


def no_inference(csp: CSP, node: str, removed: dict) -> True:
    return True


def _revise(csp: CSP, arch: tuple, removed: dict):
    constraints = csp.interested_constraints(arch[0], arch[1])
    invalid_values = set()
    revised = False
    for lvalue in csp.current_domain[arch[0]]:
        valid = False
        for rvalue in csp.current_domain[arch[1]]:
            if csp.check_constraint(constraints, {arch[0]: lvalue, arch[1]: rvalue}):
                valid = True
                break
        if not valid:
            invalid_values |= {lvalue}
    removal = set()
    for element in invalid_values:
        if element in csp.current_domain[arch[0]]:
            removal |= {element}
            revised = True
    if revised:
        csp.current_domain[arch[0]] -= removal
        removed[arch[0]] |= removal
    return revised


def create_n_queen(n: int) -> CSP:
    nqueen = CSP()
    for i in range(1, n + 1):
        var = f"x{i}"
        domain = f"1..{n + 1}"
        nqueen.add_variable(var, [domain])
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            nqueen.add_constraint(f"x{i}!=x{j}+{i - j}")
            nqueen.add_constraint(f"x{i}!=x{j}+{j - i}")
    nqueen.add_constraint("all-different")
    return nqueen


def create_n_sudoku(n: int):
    sudoku = CSP()
    nn = n * n
    for i in range(1, nn + 1):
        for j in range(1, nn + 1):
            var = f"x{i}{j}"
            domain = f"1..{nn + 1}"
            sudoku.add_variable(var, [domain])

    for i in range(1, nn + 1):
        for J in range(1, nn + 1):
            for j in range(J + 1, nn + 1):
                sudoku.add_constraint(f"x{J}{i}!=x{j}{i}")
                sudoku.add_constraint(f"x{i}{J}!=x{i}{j}")

    for xi in range(1, nn + 1):
        for xj in range(1, nn + 1):
            for yi in range(1, nn + 1):
                for yj in range(1, nn + 1):
                    if xi != yi and xj != yj and (constraint := f"x{yi}{yj}!=x{xi}{xj}") not in sudoku.constraint and \
                            ceil(xi / n) == ceil(yi / n) and ceil(xj / n) == ceil(yj / n):
                        sudoku.add_constraint(constraint)

    return sudoku


def print_sudoku(n: int, solution: dict):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            line = ""
            for I in range(1, n + 1):
                for J in range(1, n + 1):
                    line += str(solution[f"x{I + (i - 1) * n}{J + (j - 1) * n}"]) + " "
                line += "| "
            print(line[: -2])
        if i != n:
            print("-" * (n * n * 2 + (n - 1) * 2 - 1))


def print_queens(n: int, solution: dict):
    print('----' * n)
    for i in range(1, n + 1):
        line = ""
        for j in range(1, n + 1):
            line += f"| {'#' if solution[f'x{i}'] == j else ' '} "
        print(line+"|")
        print('----' * n)
