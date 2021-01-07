class CSP:
    legal_relations = {'<', '<=', '>=', '>', '!=', '='}
    legal_operations = {'+', '*'}

    def __init__(self, domains: dict = dict(), constraints: set = set()):
        self.domains = domains
        self.constraints = constraints

    def add_constraint_semplified(self, lvar: str, relation: str, rvar: str, op: str = "+", constant: str = "0"):
        # add constraint in linear form, e.g.: x1 != x2 + 2 | x1 != x2 * 3
        if lvar in self.domains.keys() and rvar in self.domains.keys() and relation in CSP.legal_relations and \
                op in CSP.legal_operations:
            self.constraints.add((lvar, relation, rvar, op, constant))
        else:
            print(f"Constraint error: {lvar + relation + rvar + op + constant}")

    def add_constraint(self, constraint: str):
        if constraint == "all-diff":
            var = list(self.domains.keys())
            for i in range(l := len(var)):
                for j in range(i + 1, l):
                    self.add_constraint_semplified(var[i], '!=', var[j])
        elif constraint == 'no-diagonal':
            var = list(self.domains.keys())
            for i in range(l := len(var)):
                for j in range(i + 1, l):
                    self.add_constraint_semplified(var[i], '!=', var[j], '+', str(i - j))
                    self.add_constraint_semplified(var[i], '!=', var[j], '+', str(j - i))

    def add_variable(self, variable_name: str, domain: list = None):
        if variable_name == "" or variable_name in self.domains.keys():
            print("Illegal varaible name")
            return
        self.domains |= {variable_name: set()}
        self.add_domain(variable_name, domain)

    def add_domain(self, var_name: str, queries: list):
        if var_name not in self.domains.keys():
            print("Wrong var name")
            return
        domain = set()
        for query in queries:
            sep = query.find('..')
            if sep != -1:
                val = {x for x in range(int(query[0: sep]), int(query[sep + 2:]) + 1)}
            else:
                val = {int(query)}
            domain |= val
        self.domains[var_name] |= domain

    def print(self):
        print("Domanis:" + str(self.domains))
        for element in self.constraints:
            print(element)


class BacktrackSolver:

    def __init__(self, csp: CSP):
        self.csp = csp
        self.state = {x: None for x in csp.domains.keys()}
        for key in self.state.keys():
            val = self.csp.domains[key].pop()
            self.csp.domains[key].add(val)
            self.state[key] = None

    def check_consistency(self, current_config: dict = None):
        if current_config is None:
            current_config = self.state
        for constraint in self.csp.constraints:
            if current_config[constraint[0]] is None or current_config[constraint[2]] is None:
                continue
            if not constraint_valid(current_config[constraint[0]], constraint[1], current_config[constraint[2]], \
                                    constraint[3], constraint[4]):
                return False
        return True

    def is_assigned(self):
        for i in self.state.values():
            if i is None:
                return False
        return True

    def solve(self):
        return self._solve()

    def _solve(self):
        if self.check_consistency() and self.is_assigned():
            return self.state
        var = self.sel_val()
        for val in self.val_order(var):
            if self.check_consistency(self.state | {var: val}):
                self.state |= {var: val}
                if inf := ac_3(self.csp, get_other_neighbours(self.csp, var, "")):
                    result = self._solve()
                    if result:
                        return result
                self.state |= {var: None}
        return False

    def val_order(self, var):
        # todo sort logic
        return list(self.csp.domains[var])

    def sel_val(self):
        maxkey = None
        maxcardinality = -1
        for key in self.csp.domains.keys():
            if l := len(self.csp.domains[key]) > maxcardinality and self.state[key] is None:
                maxcardinality = l
                maxkey = key
        return maxkey

    def print(self):
        print(self.state)
        self.csp.print()


def constraint_valid(lval: int, rel: str, rval: int, op: str, constant: str):
    constant = int(constant)
    if op == "+":
        if rel == '<=':
            return lval <= rval + constant
        elif rel == '<':
            return lval < rval + constant
        elif rel == '>=':
            return lval >= rval + constant
        elif rel == '>':
            return lval >= rval + constant
        elif rel == '!=':
            return lval != rval + constant
        elif rel == '=':
            return lval == rval + constant
    elif op == "*":
        if rel == '<=':
            return lval <= rval * constant
        elif rel == '<':
            return lval < rval * constant
        elif rel == '>=':
            return lval >= rval * constant
        elif rel == '>':
            return lval >= rval * constant
        elif rel == '!=':
            return lval != rval * constant
        elif rel == '=':
            return lval == rval * constant
    else:
        print(f"Op invalid {rel}")
        return False


def get_other_neighbours(csp: CSP, xi: str, xj: str) -> list:
    neighbours = []
    for constraint in csp.constraints:
        if (constraint[0] == xi and constraint[2] != xj) or (constraint[2] == xi and constraint[0] != xj):
            neighbours.append(constraint)
    return neighbours


def revise(csp: CSP, arch: tuple) -> bool:
    # arch = (x, op, y)
    revised = False
    for x_value in csp.domains[arch[0]]:
        exist_y = False

        # Check for xj legal val existence
        for y_value in csp.domains[arch[2]]:
            if constraint_valid(x_value, arch[1], y_value, arch[3], arch[4]):
                exist_y = True
                break
        if not exist_y:
            csp.domains[arch[0]].remove(x_value)
            revised = True
    return revised


def ac_3(csp: CSP, queue: list) -> bool:
    while len(queue) > 0:
        arch = queue.pop()
        if revise(csp, arch):
            if len(csp.domains[arch[0]]) == 0:
                return False
            for element in get_other_neighbours(csp, arch[0], arch[2]):
                queue |= element
    return True
