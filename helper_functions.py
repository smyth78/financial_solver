import pandas as pd
import json
from sympy import nsolve, Symbol, solve
from sigfig import round

import dash_bootstrap_components as dbc

import alerts

# use this for f i and p
def solve_working_equation(i, p, n, r, f, is_working):
    params = [i, p, n, r, f]
    for parameter in params:
        if type(parameter) == Symbol:
            subject_sym = parameter
    if is_working:
        eqn = -f + i * (r / 1200 + 1) ** (12 * n) + p * ((r / 1200 + 1) ** (n * 12) - 1) / (r / 1200)
    else:
        eqn = -f + i * (r / 1200 + 1) ** (12 * n) - p * ((r / 1200 + 1) ** (n * 12) - 1) / (r / 1200)
    solved = solve(eqn, subject_sym, 0)
    soln = solved[0][0]
    return float(soln)

# use this for r and n
def solve_working_equation_v2(i, p, n, r, f):
    params = [i, p, n, r, f]
    for parameter in params:
        if type(parameter) == Symbol:
            subject_sym = parameter
    eqn = -f + ((1+r/1200)**(12*n)*(i*((1+r/1200)-1)+p)-p)/((1+r/1200)-1)
    # must not guess 0!... nsolve as algebriac solution impossible
    solved = nsolve(eqn, subject_sym, 0.1)
    return float(solved)


def convert_fstrings_to_floats(fstrings):
    floats = []
    for fstring in fstrings:
        try:
            floats.append(float(fstring.replace(',', '')))
        except ValueError:
            # input box is empty
            floats.append(None)
    return floats

def convert_floats_to_ints_to_fstrings(floats):
    fstrings = []
    for number in floats:
        # first try to convert to integer
        try:
            if number.is_integer():
                fstrings.append("{:,}".format(int(number)))
            else:
                number = round(number, decimals=2)
                # if the number ends in a .0 just call it an integer
                if str(number)[-2:] == '.0':
                    fstrings.append("{:,}".format(int(number)))
                else:
                    fstrings.append("{:,}".format(float(number)))
        # if input box is empty
        except AttributeError:
            fstrings.append('')
    return fstrings


