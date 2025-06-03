
from random import shuffle
from unittest import removeResult


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                results  = self.recursive_backtracking(assignment)
                if results is not None:
                    return results
                    assignment.pop(var)
        return None


    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_sudoAmerica_csp():
    # South American countries as variables with abbreviations
    AR, BO, BR, CL, CO, EC, GY, PY, PE, SR, UY, VE = (
        'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname',
        'Uruguay', 'Venezuela')

    # Available colors
    colors = ['Red', 'Green', 'Blue', 'Yellow']

    # Domains for each country
    domains = {
        AR: colors[:], BO: colors[:], BR: colors[:], CL: colors[:], CO: colors[:],
        EC: colors[:], GY: colors[:], PY: colors[:], PE: colors[:], SR: colors[:],
        UY: colors[:], VE: colors[:]
    }

    # Neighbor relationships based on the map
    neighbours = {
        AR: [BO, BR, CL, PY, UY],
        BO: [AR, BR, CL, PY, PE],
        BR: [AR, BO, CO, GY, PY, PE, SR, UY, VE],
        CL: [AR, BO, PE],
        CO: [BR, EC, PE, VE],
        EC: [CO, PE],
        GY: [BR, SR, VE],
        PY: [AR, BO, BR],
        PE: [BO, BR, CL, CO, EC],
        SR: [BR, GY],
        UY: [AR, BR],
        VE: [BR, CO, GY]
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    # Constraints for each country
    constraints = {
        AR: constraint_function, BO: constraint_function, BR: constraint_function, CL: constraint_function,
        CO: constraint_function,
        EC: constraint_function, GY: constraint_function, PY: constraint_function, PE: constraint_function,
        SR: constraint_function,
        UY: constraint_function, VE: constraint_function
    }

    return CSP([AR, BO, BR, CL, CO, EC, GY, PY, PE, SR, UY, VE], domains, neighbours, constraints)


if __name__ == '__main__':
    sudoAmerica = create_sudoAmerica_csp()
    result = sudoAmerica.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
