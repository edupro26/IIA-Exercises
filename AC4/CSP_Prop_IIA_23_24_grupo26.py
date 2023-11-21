"""
    Avaliação Contínua 4

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""

from logic import *
from csp import *

def csp_prop(formulas):

    # Get variables from formulas
    variables = get_variables(formulas)

    # Get domains from formulas
    domains = get_domains(formulas, variables)

    # Get neighbors from formulas
    neighbors = get_neighbors(formulas, variables)

    constraints = None  # TODO

    return CSP(variables, domains, neighbors, constraints)


def get_neighbors(formulas, variables):
    neighbors = {var: set() for var in variables}

    forms_cnf = []
    for form in formulas:
        cnf = [to_cnf(str(form))]
        cnf_args = dissociate('&', cnf)
        for arg in cnf_args:
            forms_cnf.append(arg)

    for form in forms_cnf:
        symbols = prop_symbols(form)
        for var1 in symbols:
            for var2 in symbols:
                if var1.op != var2.op:
                    neighbors[var1.op].add(var2.op)

    return neighbors


def get_domains(formulas, variables):
    domains = dict()
    for var in variables:
        domains[var] = [False, True]
    for var in formulas:
        if is_prop_symbol(var.op):
            domains[var.op] = [True]
        if var.op == '~' and len(var.args) < 2:
            domains[var.args[0].op] = [False]
    return domains


def get_variables(formulas):
    variables = []
    for form in formulas:
        symbols = prop_symbols(form)
        for j in symbols:
            if j.op not in variables:
                variables.append(j.op)
    variables.sort()
    return variables


# ___________________________________________________________________________________
# TESTS

# 1.
try:
    formulas={expr('A ==> (B & C)'),expr('A')}
    abc_csp=csp_prop(formulas)
    print(abc_csp.variables)
except Exception as e:
    print(repr(e))

# 2.
try:
    formulas={expr('A ==> (B & C)'),expr('A')}
    abc_csp=csp_prop(formulas)
    print(sorted([(var,sorted(val)) for (var,val) in abc_csp.domains.items()]))
except Exception as e:
    print(repr(e))

# 3.
try:
    formulas={expr('A ==> (B & C)'),expr('A')}
    abc_csp=csp_prop(formulas)
    print(sorted([(var,sorted(val)) for (var,val) in abc_csp.neighbors.items()]))
except Exception as e:
    print(repr(e))

# 4.
try:
    formulas={expr('A & ~A')}
    a_csp=csp_prop(formulas)
    print(sorted([(var,sorted(val)) for (var,val) in a_csp.neighbors.items()]))
except Exception as e:
    print(repr(e))