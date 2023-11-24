"""
    Avaliação Contínua 4

    Grupo 26:
    Eduardo Proença 57551
    Alexandre Pinto 55958
"""

from logic import *
from csp import *

def csp_prop(formulas):

    def constraints(A, a, B, b):
        eval = True
        model = {A: a, B: b}
        for form in forms_cnf:
            if eval:
                vars = {var.op for var in prop_symbols(form)}
                if len(vars) > 1 and A in vars and B in vars:
                    eval = pl_true(form, {expr(A): model[A], expr(B): model[B]})
                elif len(vars) == 1 and A in vars:
                    eval = pl_true(form, {expr(A): model[A]})
                elif len(vars) == 1 and B in vars:
                    eval = pl_true(form, {expr(B): model[B]})
        return eval

    # Get variables, domains and neighbors
    variables = get_variables(formulas)
    domains = get_domains(formulas, variables)
    forms_cnf = convert_to_cnf(formulas)
    neighbors = get_neighbors(forms_cnf, variables)

    return CSP(variables, domains, neighbors, constraints)


def convert_to_cnf(formulas):
    forms_cnf = set()
    for form in formulas:
        cnf = [to_cnf(str(form))]
        cnf_args = dissociate('&', cnf)
        forms_cnf.update(cnf_args)
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
    domains = {var: [False, True] for var in variables}
    for var in formulas:
        if is_prop_symbol(var.op):
            domains[var.op] = [True]
        if var.op == '~' and len(var.args) < 2:
            domains[var.args[0].op] = [False]
    return domains


def get_variables(formulas):
    variables = set()
    for form in formulas:
        symbols = prop_symbols(form)
        variables.update([j.op for j in symbols])
    return sorted(variables)
