class CSP:

    def __init__(self, domains: dict = dict(), constraints: set = set()):
        self.domains = domains
        self.constraints = constraints

    def add_constraint(self, constraint: str):
        if constraint != "all-diff":
            self.constraints |= {constraint}
        else:
            for i in self.domains.keys():
                for j in self.domains.keys():
                    if i != j:
                        self.add_constraint(f"{i}!={j}")

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
        print("Constraints" + str(self.constraints))


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
        cons = True
        for constraint in self.csp.constraints:
            c = str(constraint)
            c.replace(" ", "")
            if c.find('<=') != -1:
                if current_config[c[: c.find('<=')]] > current_config[c[c.find('<=') + 2:]] and \
                        current_config[c[: c.find('<=')]] is not None and current_config[c[c.find('<=') + 2:]] is not None:
                    cons = False
                    break
            elif c.find('>=') != -1:
                if current_config[c[: c.find('>=')]] < current_config[c[c.find('>=') + 2:]] and \
                        current_config[c[: c.find('>=')]] is not None and current_config[c[c.find('>=') + 2:]] is not None:
                    cons = False
                    break
            elif c.find('==') != -1:
                if current_config[c[: c.find('==')]] != current_config[c[c.find('==') + 2:]] and \
                        current_config[c[: c.find('==')]] is not None and current_config[c[c.find('==') + 2:]] is not None:
                    cons = False
                    break
            elif c.find('!=') != -1:
                if current_config[c[: c.find('!=')]] == current_config[c[c.find('!=') + 2:]] and \
                        current_config[c[: c.find('!=')]] is not None and current_config[c[c.find('!=') + 2:]] is not None:
                    cons = False
                    break
            elif c.find('<') != -1:
                if current_config[c[: c.find('<')]] >= current_config[c[c.find('<') + 2:]] and \
                        current_config[c[: c.find('<')]] is not None and current_config[c[c.find('<') + 2:]] is not None:
                    cons = False
                    break
            elif c.find('>') != -1:
                if current_config[c[: c.find('>')]] <= current_config[c[c.find('>') + 2:]] and \
                        current_config[c[: c.find('>')]] is not None and current_config[c[c.find('>') + 2:]] is not None:
                    cons = False
                    break
            elif c.find('=') != -1:
                if current_config[c[: c.find('=')]] != current_config[c[c.find('=') + 2:]] and \
                        current_config[c[: c.find('=')]] is not None and current_config[c[c.find('=') + 2:]] is not None:
                    cons = False
                    break
            else:
                print('Constraint error: ' + constraint)
                cons = False
                break
        return cons

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
                # inf = self.inference(var, val)
                inf = True
                if inf:
                    result = self._solve()
                    if result is not False:
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
            if len(self.csp.domains[key]) > maxcardinality:
                maxcardinality = len(self.csp.domains[key])
                maxkey = key
        return maxkey

    def print(self):
        print(self.state)
        self.csp.print()
