from random import shuffle
from math import inf
from operator import itemgetter


class CSP_cryptomath:

    def __init__(self, word1: str = 'SEND', word2: str = 'MORE', word3: str = 'MONEY'):
        word1 = word1.upper()
        word2 = word2.upper()
        word3 = word3.upper()

        self.selected = set()
        self.count = 0

        self.domain = dict()
        self.constraint = set()
        self.state = dict()

        for letter in (word1 + word2 + word3):
            self.domain |= {letter: {x for x in range(0, 10)}}
            self.state |= {letter: None}
        w1 = word1[::-1]
        w2 = word2[::-1]
        w3 = word3[::-1]
        s = ""
        for e in self.domain.keys():
            s += e
        self.constraint |= {f"{word1[0]}!=0"}
        self.constraint |= {f"{word2[0]}!=0"}
        self.constraint |= {f"{word3[0]}!=0"}
        length = max(len(w1), len(w2), len(w3))
        query = ""
        left = ""
        right = ""
        for i in range(l := len(d := [x for x in self.domain.keys()])):
            for j in range(i + 1, l):
                self.constraint |= {f"{d[i]}!={d[j]}"}

            left += f"({w1[i] if i < len(w1) else 0}+{w2[i] if i < len(w2) else 0})*10^{i}+"
            right += f"({w3[i] if i < len(w3) else 0})+"
        left = left[:-1]
        right = right[:-1]
        self.constraint |= {left + '==' + right}

        # for i in range(length):
        #     if i == 0:
        #         self.constraint |= {f"{w1[i] if len(w1) > i else '0'}+{w2[i] if len(w2) > i else '0'}=={w3[i] if len(w3) > i else '0'}"}
        #     else:
        #         self.constraint |= {
        #             f"{w1[i] if len(w1) > i else '0'}+{w2[i] if len(w2) > i else '0'}+int(({w1[i - 1] if len(w1) > i - 1 else '0'}+{w2[i - 1] if len(w2) > i - 1 else '0'})/10)=={w3[i] if len(w3) > i else '0'}"}

    def insert_val(self, constraint: str, state):
        for key in state.keys():
            constraint = constraint.replace(key, str(state[key]))
        return constraint

    def complete_assigned(self):
        for val in self.state.values():
            if val is None:
                return False
        return True

    def check_constraint(self, constraint_set: set, temp_assign: dict = None):
        state = self.state
        if temp_assign is not None:
            state |= temp_assign
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


class CSP_magicsequence:

    def __init__(self, sequence_length: int):

        self.domain = {}
        self.count = 0

        self.domain = dict()
        self.constraint = set()
        self.state = dict()

        for i in range(sequence_length):
            self.domain |= {f"S{i}": {x for x in range(sequence_length)}}
            self.state |= {f"S{i}": None}
            sumpositive = ""
        for i in range(l := len(self.domain.keys())):
            sumpositive += f"S{i}+"
            query = f"S{i}=="
            for j in range(l):
                query += f"1*(S{j}=={i})+"
            query = query[: -1]
            self.constraint |= {query}
        self.constraint |= {sumpositive[: -1]+"!=0"}

    def insert_val(self, constraint: str, state):
        for key in state.keys():
            constraint = constraint.replace(key, str(state[key]))
        return constraint

    def complete_assigned(self):
        for val in self.state.values():
            if val is None:
                return False
        return True

    def check_constraint(self, constraint_set: set, temp_assign: dict = None):
        state = self.state
        if temp_assign is not None:
            state |= temp_assign
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


def sel_var(csp: CSP_cryptomath):
    minkey = None
    mincardinality = inf
    minconstraints = -1
    for key in csp.domain.keys():
        if (cardinality := len(csp.domain[key])) <= mincardinality and csp.state[key] is None:
            if cardinality == mincardinality and csp.constraints_cardinality(key) <= minconstraints:
                continue
            mincardinality = cardinality
            minconstraints = csp.constraints_cardinality(key)
            minkey = key
    return minkey


def val_order(csp: CSP_cryptomath, var: str):
    result = list(csp.domain[var])
    shuffle(result)
    return result


def backtrack(csp: CSP_cryptomath):
    csp.count += 1
    if csp.check_constraint(csp.constraint) and csp.complete_assigned():
        return csp.state
    var = sel_var(csp)
    for val in val_order(csp, var):
        if csp.check_constraint(csp.constraint, {var: val}):
            csp.state |= {var: val}
            # if ac_3(csp, var):
            if True:
                result = backtrack(csp)
                if result:
                    return result
        csp.state |= {var: None}
    return False


def ac_3(csp: CSP_cryptomath, node: str):
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


def revise(csp: CSP_cryptomath, constraint: str):
    revised = False
    # for
