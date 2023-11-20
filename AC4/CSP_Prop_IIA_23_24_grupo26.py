"""
    Avaliação Contínua 4

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""

from logic import *
from csp import *

def csp_prop(formulas):
    variables = []
    domains = dict()
    neighbors = None
    constraints = None

    # Get variables and domains
    for i in formulas:
        symbols = prop_symbols(i)
        for j in symbols:
            possible_values = [False, True]
            if j.op not in variables:
                variables.append(j.op)
                variables.sort()
                if is_prop_symbol(i.op):
                    domains[j.op] = True # Not working needs fixing
                else:
                    domains[j.op] = possible_values

    csp = CSP(variables, domains, neighbors, constraints)
    return csp


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