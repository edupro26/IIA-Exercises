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
    for i in formulas:
        symbols = prop_symbols(i)
        for j in symbols:
            if j.op not in variables:
                variables.append(j.op)

    variables.sort()
    csp = CSP(variables, None, None, None)
    return csp


try:
    formulas={expr('A ==> (B & C)'),expr('A')}
    abc_csp=csp_prop(formulas)
    print(abc_csp.variables)
except Exception as e:
    print(repr(e))