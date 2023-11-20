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

    neighbors = None  # TODO
    constraints = None  # TODO

    return CSP(variables, domains, neighbors, constraints)


def get_domains(formulas, variables):
    domains = dict()
    for i in variables:
        domains[i] = [False, True]
    for i in formulas:
        if is_prop_symbol(i.op):
            domains[i.op] = [True]
        if i.op == '~' and len(i.args) < 2:
            domains[i.args[0].op] = [False]
    return domains


def get_variables(formulas):
    variables = []
    for i in formulas:
        symbols = prop_symbols(i)
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
#try:
#    formulas={expr('A ==> (B & C)'),expr('A')}
#    abc_csp=csp_prop(formulas)
#    print(sorted([(var,sorted(val)) for (var,val) in abc_csp.neighbors.items()]))
#except Exception as e:
#    print(repr(e))