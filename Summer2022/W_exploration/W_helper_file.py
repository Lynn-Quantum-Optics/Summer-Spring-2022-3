import numpy as np
import math
import sympy as sym
from sympy.physics.quantum.dagger import Dagger
from sympy.functions import conjugate
from sympy import sin, cos, simplify, I, pi, Trace, Matrix, re, trigsimp, Number, N
import pandas as pd
import scipy.optimize as spo
from sympy.utilities.lambdify import lambdify

def range_with_floats(start, stop, step):
    while stop > start:
        yield start
        start += step

def complex_round(num):
    # chop = True makes very small numbers 0
    num = N(num, chop = True)
    try:
        round(num, 5)
        return round(num, 5)
    except TypeError:
        print('\n looping complex_round', num, '\n')
        return complex_round(re(num))

# Could be useful in the future
# def round_expr(expr, num_digits):
#     return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})

"""
Normalizes state so that overall probability equals 1
"""
def normalize_state(state):
    mag = complex_round(conjugate(state[0])*state[0] + conjugate(state[1])*state[1] 
        + conjugate(state[2])*state[2] + conjugate(state[3])*state[3])

    if mag == 1:
        return state
    elif mag != 0:
        return (1/math.sqrt(mag))*state
    else:
        raise Exception("Magnitude of state is 0, can't normalize state")

def partial_transpose(rho):
    #Swap values to create partial transpose
    rho[1, 0], rho[0, 1] = rho[0, 1], rho[1, 0]
    rho[1, 2], rho[0, 3] = rho[0, 3], rho[1, 2]
    rho[3, 0], rho[2, 1] = rho[2, 1], rho[3, 0]
    rho[3, 2], rho[2, 3] = rho[2, 3], rho[3, 2]
    
    return rho

"""
Returns true if the partial transpose has negative eigenvalue i.e entangled
"""
def PPT_test(rho):
    #Swap values to create partial transpose
    rho[1, 0], rho[0, 1] = rho[0, 1], rho[1, 0]
    rho[1, 2], rho[0, 3] = rho[0, 3], rho[1, 2]
    rho[3, 0], rho[2, 1] = rho[2, 1], rho[3, 0]
    rho[3, 2], rho[2, 3] = rho[2, 3], rho[3, 2]
    
    rho_eigenvals = list(rho.eigenvals().keys())
    rho_eigenvals = [complex_round(eig) for eig in rho_eigenvals]

    if min(rho_eigenvals) < 0:
        return True
    else:
        return False

"""
Calculates the tangle and concurrence of an theoretical density matrix
tangle = 0 for seperable states and tangle = 1 for Bell States
"""
def theor_tangle(state):
    state = normalize_state(state)

    rho = state*Dagger(state)

    if round(simplify(Trace(rho)), 5) != 1:
        raise Exception("Trace of rho is not 1, invalid density matrix")

    sigma = Matrix([[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]])
    R = rho*sigma*(rho.T)*sigma

    R_eigenvals = R.eigenvals()
    R_eig = list(R_eigenvals.keys())
    R_mult = list(R_eigenvals.values())
    if len(R_eigenvals) ==1:
        R_eig = [R_eig[0]]*(R_mult[0])
    elif len(R_eigenvals) ==2:
        R_eig = [R_eig[0]]*(R_mult[0]) + [R_eig[1]]*(R_mult[1])
    elif len(R_eigenvals) ==3:
        R_eig = [R_eig[0]]*(R_mult[0]) + [R_eig[1]]*(R_mult[1]) + [R_eig[2]]*(R_mult[2])
    else:
        R_eig = [R_eig[0]]*(R_mult[0]) + [R_eig[1]]*(R_mult[1]) + [R_eig[2]]*(R_mult[2]) + [R_eig[3]]*(R_mult[3])
    
    R_eig = [abs(x) for x in R_eig]
    R_eig.sort(reverse=True) # sort in descending order
    c = math.sqrt(R_eig[0]) - math.sqrt(R_eig[1]) - math.sqrt(R_eig[2]) - math.sqrt(R_eig[3])
    concurrence = max(0, c)
    
    tangle = concurrence**2

    return complex_round(tangle)

"""
Finds the minimum value for the Original 6 Witnesses and prime witnesses seperately
"""
def optimize_Wp(Wp):
    func = lambdify((x,phi), re(Wp))
    def my_func(x):
        return func(*tuple(x))

    Wp_optimize = spo.minimize(my_func,[pi,pi], bounds = [(0,2*pi), (0,2*pi)])

    if Wp_optimize.success:
        return complex_round(Wp_optimize.fun)
    else:
        return "n/o"

def optimize_W(W):
    func = lambdify((x), re(W))
    def my_func(x):
        return func(*tuple(x))

    W_optimize = spo.minimize(my_func,[pi], bounds = [(0,2*pi)])

    if W_optimize.success:
        return complex_round(W_optimize.fun)
    else:
        # if the value is 1000, not optimizable
        return 1000


# Exploration of Detectability of all prime witnesses
phi = sym.Symbol('phi', real=True)
x = sym.Symbol('x', real=True)

phi_plus = 1/math.sqrt(2) * Matrix([[1],[0],[0],[1]])
phi_minus = 1/math.sqrt(2) * Matrix([[1],[0],[0],[-1]])
psi_plus = 1/math.sqrt(2) * Matrix([[0],[1],[1],[0]])
psi_minus = 1/math.sqrt(2) * Matrix([[0],[1],[-1],[0]])

#/////////////////////////////////////////// Original 6 Witnesses /////////////////////////////////////////////
psi_1 = cos(x)*phi_plus + sin(x)*phi_minus
W1 = partial_transpose(psi_1*Dagger(psi_1))

psi_2 = cos(x)*psi_plus + sin(x)*psi_minus
W2 = partial_transpose(psi_2*Dagger(psi_2))

psi_3 = cos(x)*phi_plus + sin(x)*psi_plus
W3 = partial_transpose(psi_3*Dagger(psi_3))

psi_4 = cos(x)*phi_minus + sin(x)*psi_minus
W4 = partial_transpose(psi_4*Dagger(psi_4))

psi_5 = cos(x)*phi_plus + I*sin(x)*psi_minus
W5 = partial_transpose(psi_5*Dagger(psi_5))

psi_6 = cos(x)*phi_minus + I*sin(x)*psi_plus
W6 = partial_transpose(psi_6*Dagger(psi_6))

#////////////////////////////////////////// Eritas's Witnesses ///////////////////////////////////////////////
"""
Note: complex exponential is in trig form because sympy doesn't seem to simplify expressions with complex exponentials well
"""

psi_1p = Matrix([[cos(x)],[0],[0],[(I*sin(phi) + cos(phi))*sin(x)]])
W1p = partial_transpose(psi_1p*Dagger(psi_1p))

psi_2p = Matrix([[0],[cos(x)],[(I*sin(phi) + cos(phi))*sin(x)],[0]])
W2p = partial_transpose(psi_2p*Dagger(psi_2p))

psi_3p = cos(x)*phi_plus + (I*sin(phi) + cos(phi))*sin(x)*psi_plus
W3p = partial_transpose(psi_3p*Dagger(psi_3p))

psi_4p = cos(x)*phi_minus + (I*sin(phi) + cos(phi))*sin(x)*psi_minus
W4p = partial_transpose(psi_4p*Dagger(psi_4p))

psi_5p = cos(x)*phi_plus + (I*sin(phi) + cos(phi))*sin(x)*psi_minus
W5p = partial_transpose(psi_5p*Dagger(psi_5p))

psi_6p = cos(x)*phi_minus + (I*sin(phi) + cos(phi))*sin(x)*psi_plus
W6p = partial_transpose(psi_6p*Dagger(psi_6p))




