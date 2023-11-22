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
    forms_cnf = convert_to_cnf(formulas)
    neighbors = get_neighbors(forms_cnf, variables)

    def constraints(var1, value1, var2, value2):
        eval = True
        for form in forms_cnf:
            if not eval:
                return eval
            temp = prop_symbols(form)
            vars = [var for var in temp]
            vars.sort()
            if len(vars) > 1:
                if var1 == vars[0].op and var2 == vars[1].op:
                    eval = pl_true(form, {vars[0]: value1, vars[1]: value2})
                elif var1 == vars[1].op and var2 == vars[0].op:
                    eval = pl_true(form, {vars[0]: value2, vars[1]: value1})
            else:
                if var1 == vars[0].op:
                    eval = pl_true(form, {vars[0]: value1})
                elif var2 == vars[0].op:
                    eval = pl_true(form, {vars[0]: value2})
        return eval

    return CSP(variables, domains, neighbors, constraints)


def convert_to_cnf(formulas):
    forms_cnf = []
    for form in formulas:
        cnf = [to_cnf(str(form))]
        cnf_args = dissociate('&', cnf)
        for arg in cnf_args:
            forms_cnf.append(arg)
    return forms_cnf


def get_neighbors(formulas, variables):
    neighbors = {var: set() for var in variables}
    for form in formulas:
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

# 5.
try:
    formulas={expr('A ==> (B & C)'),expr('A')}
    abc_csp=csp_prop(formulas)
    r = backtracking_search(abc_csp)
    print('Assignment = ',r)
except Exception as e:
    print(repr(e))

# 6.
try:
    formulas={expr('VA | VP'),expr('AV | AP'),expr('PV | PA'),expr('VP'),expr('VA ==> ~VP'),expr('AP ==> ~AV'),
              expr('PA ==> ~PV'),expr('VA ==> ~PA'),expr('PV ==> ~AV'),expr('VP ==> ~AP')}
    dancam_csp=csp_prop(formulas)
    r = backtracking_search(dancam_csp)
    print('Assignment = ',r)
except Exception as e:
    print(repr(e))