import itertools
from pprint import pformat


class Variable:
    def __init__(self, name, assignments, cpt, parents=[]):
        self.name = name
        self.assignments = assignments
        self.assignment_idx = {val: i for i, val in enumerate(assignments)}
        self.cpt = cpt
        self.parents = parents

    def get_probability(self, value, parent_values):
        key = tuple(parent_values[p.name] for p in self.parents)
        return self.cpt[key][self.assignment_idx[value]]


class BayesianNetwork:
    def __init__(self, variables):
        self.variables = variables
        self.var_map = {v.name: v for v in variables}

    def get_joint_probability(self, assignment):
        prob = 1.0
        for var in self.variables:
            parent_vals = {p.name: assignment[p.name] for p in var.parents}
            prob *= var.get_probability(assignment[var.name], parent_vals)
        return prob

    def get_conditional_probability(self, query, evidence):
        all_vars = [v.name for v in self.variables]
        hidden_vars_numerator = [v for v in all_vars if v not in query and v not in evidence]
        hidden_vars_denominator = [v for v in all_vars if v not in evidence]

        # Numerator: P(query ∩ evidence)
        numerator = 0.0
        for vals in itertools.product(['false', 'true'], repeat=len(hidden_vars_numerator)):
            hidden_assignment = dict(zip(hidden_vars_numerator, vals))
            full = {**hidden_assignment, **query, **evidence}
            numerator += self.get_joint_probability(full)

        # Denominator: P(evidence)
        denominator = 0.0
        for vals in itertools.product(['false', 'true'], repeat=len(hidden_vars_denominator)):
            hidden_assignment = dict(zip(hidden_vars_denominator, vals))
            full = {**hidden_assignment, **evidence}
            denominator += self.get_joint_probability(full)

        return numerator / denominator if denominator > 0 else 0


def print_conditional_probability(network, query, evidence):
    print("Given:")
    print(pformat(evidence))
    print("Conditional probability of:")
    print(pformat(query))
    result = network.get_conditional_probability(query, evidence)
    print(f"=> Result: {result:.4f}  (≈ {round(result * 100)}%)")


def build_homework_network():
    # CPTs
    dt = Variable('DT', ['false', 'true'], {(): [0.7, 0.3]})
    em = Variable('EM', ['false', 'true'], {(): [0.7, 0.3]})
    ftl = Variable('FTL', ['false', 'true'], {(): [0.8, 0.2]})
    v = Variable('V', ['false', 'true'], {
        ('true',): [0.7, 0.3],
        ('false',): [0.1, 0.9]
    }, parents=[dt])
    sms = Variable('SMS', ['false', 'true'], {
        ('true', 'true'): [0.05, 0.95],
        ('true', 'false'): [0.6, 0.4],
        ('false', 'true'): [0.3, 0.7],
        ('false', 'false'): [0.7, 0.3]
    }, parents=[dt, em])
    hc = Variable('HC', ['false', 'true'], {
        ('true', 'true', 'true'): [0.1, 0.9],
        ('true', 'true', 'false'): [0.2, 0.8],
        ('true', 'false', 'true'): [0.7, 0.3],
        ('true', 'false', 'false'): [0.8, 0.2],
        ('false', 'true', 'true'): [0.4, 0.6],
        ('false', 'true', 'false'): [0.5, 0.5],
        ('false', 'false', 'true'): [0.9, 0.1],
        ('false', 'false', 'false'): [0.99, 0.01],
    }, parents=[dt, ftl, em])

    return BayesianNetwork([dt, em, ftl, v, sms, hc])


if __name__ == '__main__':
    net = build_homework_network()
    print_conditional_probability(net, {'FTL': 'true'}, {'HC': 'true'})