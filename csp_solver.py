from random import shuffle
from math import inf


class CSP:

    def __init__(self):

        self.domain = dict()
        self.constraint = set()
        self.state = dict()

        # for letter in (word1 + word2 + word3):
        #     self.domain |= {letter: {x for x in range(0, 10)}}
        #     self.state |= {letter: None}
        # w1 = word1[::-1]
        # w2 = word2[::-1]
        # w3 = word3[::-1]
        # s = ""
        # for e in self.domain.keys():
        #     s += e
        # self.constraint |= {f"{word1[0]}!=0"}
        # self.constraint |= {f"{word2[0]}!=0"}
        # self.constraint |= {f"{word3[0]}!=0"}
        # length = max(len(w1), len(w2), len(w3))
        # query = ""
        # left = ""
        # right = ""
        # for i in range(l := len(d := [x for x in self.domain.keys()])):
        #     for j in range(i + 1, l):
        #         self.constraint |= {f"{d[i]}!={d[j]}"}
        #
        #     left += f"({w1[i] if i < len(w1) else 0}+{w2[i] if i < len(w2) else 0})*10^{i}+"
        #     right += f"({w3[i] if i < len(w3) else 0})+"
        # left = left[:-1]
        # right = right[:-1]
        # self.constraint |= {left + '==' + right}

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
                if constraint.find(key) != -1 and state[key] is None:
                    skip = True
                    break
            if skip:
                continue
            cop = constraint
            constraint = self.insert_val(constraint, state)
            if not eval(constraint):
                print(cop, constraint)
                return False
        return True

    def relevant_constraint(self, key) -> set:
        result = set()
        for cons in self.constraint:
            if cons.find(key) != -1:
                result |= {cons}
        return result

    def interested_constraints(self, xi: str, neighbours: set):
        queue = {}
        for cons in self.constraint:
            for key in self.domain.keys():
                if cons.find(xi) != -1 and cons.find(key) != -1:
                    queue |= {cons}
                    break
        return queue

    def constraints_cardinality(self, key):
        count = 0
        for cons in self.constraint:
            if cons.find(key) != -1:
                count += 1
        return count

    # todo util?
    @staticmethod
    def insert_val(constraint: str, state):
        for key in state.keys():
            constraint = constraint.replace(key, str(state[key]))
        return constraint


# class CSP_magicsequence:
#
#     def __init__(self, sequence_length: int):
#
#         self.domain = {}
#         self.count = 0
#
#         self.domain = dict()
#         self.constraint = set()
#         self.state = dict()
#
#         for i in range(sequence_length):
#             self.domain |= {f"S{i}": {x for x in range(sequence_length)}}
#             self.state |= {f"S{i}": None}
#             sumpositive = ""
#         for i in range(l := len(self.domain.keys())):
#             sumpositive += f"S{i}+"
#             query = f"S{i}=="
#             for j in range(l):
#                 query += f"1*(S{j}=={i})+"
#             query = query[: -1]
#             self.constraint |= {query}
#         self.constraint |= {sumpositive[: -1] + "!=0"}
#
#     def insert_val(self, constraint: str, state):
#         for key in state.keys():
#             constraint = constraint.replace(key, str(state[key]))
#         return constraint
#
#     def complete_assigned(self):
#         for val in self.state.values():
#             if val is None:
#                 return False
#         return True
#
#     def check_constraint(self, constraint_set: set, temp_assign: dict = None):
#         state = self.state
#         if temp_assign is not None:
#             state |= temp_assign
#         for constraint in constraint_set:
#             skip = False
#             for key in state.keys():
#                 if constraint.find(key) != -1 and state[key] is None:
#                     skip = True
#                     break
#             if skip:
#                 continue
#             cop = constraint
#             constraint = self.insert_val(constraint, state)
#             if not eval(constraint):
#                 return False
#         return True
#
#     def relevant_constraint(self, key) -> set:
#         result = set()
#         for cons in self.constraint:
#             if cons.find(key) != -1:
#                 result |= {cons}
#         return result
#
#     def interested_constraints(self, xi: str, neighbours: set):
#         queue = {}
#         for cons in self.constraint:
#             for key in self.domain.keys():
#                 if cons.find(xi) != -1 and cons.find(key) != -1:
#                     queue |= {cons}
#                     break
#         return queue
#
#     def constraints_cardinality(self, key):
#         count = 0
#         for cons in self.constraint:
#             if cons.find(key) != -1:
#                 count += 1
#         return count


def sel_var(csp: CSP):
    minkey = None
    min_cardinality = inf
    min_constraints = -1
    for key in csp.domain.keys():
        if (cardinality := len(csp.domain[key])) <= min_cardinality and csp.state[key] is None:
            if cardinality == min_cardinality and csp.constraints_cardinality(key) <= min_constraints:
                continue
            min_cardinality = cardinality
            min_constraints = csp.constraints_cardinality(key)
            minkey = key
    return minkey


def val_order(csp: CSP, var: str):
    result = list(csp.domain[var])
    shuffle(result)
    return result


def backtrack(csp: CSP):
    if csp.check_constraint(csp.constraint) and csp.complete_assigned():
        return csp.state
    var = sel_var(csp)
    for val in val_order(csp, var):
        if csp.check_constraint(csp.constraint, csp.state | {var: val}):
            csp.state |= {var: val}
            # if ac_3(csp, var):
            if True:
                result = backtrack(csp)
                if result:
                    return result
        csp.state |= {var: None}
    return False


def ac_3(csp: CSP, node: str):
    queue = csp.relevant_constraint(node)
    while len(queue) > 0:
        constraint = queue.pop()
        interested_nodes = {}
        for key in csp.domain.keys():
            if constraint.find(key) != -1:
                interested_nodes |= {key}
        if revise(csp, constraint):
            if len(csp.domain[node]) == 0:
                return False
            queue |= csp.interested_constraints(node, csp.domain.keys() - interested_nodes)
    return True


def revise(csp: CSP, constraint: str):
    revised = False
    # for


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

    for I in range(1, n + 1):
        for J in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    for ii in range(1, n + 1):
                        for jj in range(1, n + 1):
                            if i != ii or j != jj:
                                constraint = f"x{n * (I - 1) + i}{n * (J - 1) + j}!=x{n * (I - 1) + ii}{n * (J - 1) + jj}"
                                sudoku.add_constraint(constraint)

    return sudoku


def print_sudoku(n: int, solution: dict):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            line = ""
            for I in range(1, n + 1):
                for J in range(1, n + 1):
                    line += f"x{I + (i - 1)*n}{J + (j - 1)*n} "
                line += "| "
                line = CSP.insert_val(line, solution)
            print(line+"\n-------------------------------------")
