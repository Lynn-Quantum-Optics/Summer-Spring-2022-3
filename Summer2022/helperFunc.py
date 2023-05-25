# The code process the data from ExperimentsAutomated.py
# c is based on the dictionary created when you call get_c4() on file with Expt Purity
# can find c by running c = get_c4()
# Authors: Eritas, Becca, Ben

import numpy as np
import pandas as pd
import math
import scipy.optimize as spo
from compile_measurements import *

# Call get_c4 to get a dictionary of the coincidence counts

# c is based on the dictionary created when you call get_c4() on file with Expt Purity
# "Purity": return |P(DD) + P(AA) - P(AD) - P(DA)|/(P(DD) + P(AA) + P(AD) + P(DA))
def purity(c):
    return abs(c['DD'] + c['AA'] - c['AD'] - c['DA']) / (c['DD'] + c['AA'] + c['AD'] + c['DA'])

# c is based on the dictionary created when you call get_c4() on file with Expt Purity
def purity_from_rho(c):
    rho = densityMatrix(c)
    rho_squared = np.matmul(rho, rho)
    return np.trace(rho_squared)

# "Full_Tomography": return a 4 by 4 density matrix
def densityMatrix(c):
    # Four Pauli matrices
    sig0 = np.array([[1,0],[0,1]])
    sig1 = np.array([[0,1],[1,0]])
    sig2 = np.array([[0,-1j],[1j,0]])
    sig3 = np.array([[1,0],[0,-1]])
    pauli = [sig0] + [sig1] + [sig2] + [sig3]
    
    # Stokes Parameters:
    stokesCoeff = [1, # S00
    (c['DD'] - c['DA'] - c['AA'] + c['AD']) / (c['DD'] + c['DA'] + c['AA'] + c['AD']),  # S01
    (c['RR'] + c['LR'] - c['LL'] - c['RL']) / (c['RR'] + c['LR'] + c['LL'] + c['RL']),  # S02 
    (c['HH'] - c['HV'] - c['VV'] + c['VH']) / (c['HH'] + c['HV'] + c['VV'] + c['VH']),  # S03
    (c['DD'] - c['AD'] - c['AA'] + c['DA']) / (c['DD'] + c['AD'] + c['AA'] + c['DA']),  # S10
    (c['DD'] - c['DA'] - c['AD'] + c['AA']) / (c['DD'] + c['DA'] + c['AD'] + c['AA']),  # S11
    (c['DR'] - c['DL'] - c['AR'] + c['AL']) / (c['DR'] + c['DL'] + c['AR'] + c['AL']),  # S12
    (c['DH'] - c['DV'] - c['AH'] + c['AV']) / (c['DH'] + c['DV'] + c['AH'] + c['AV']),  # S13
    (c['RR'] + c['RL'] - c['LL'] - c['LR']) / (c['RR'] + c['RL'] + c['LL'] + c['LR']),  # S20
    (c['RD'] - c['RA'] - c['LD'] + c['LA']) / (c['RD'] + c['RA'] + c['LD'] + c['LA']),  # S21
    (c['RR'] - c['RL'] - c['LR'] + c['LL']) / (c['RR'] + c['RL'] + c['LR'] + c['LL']),  # S22
    (c['RH'] - c['RV'] - c['LH'] + c['LV']) / (c['RH'] + c['RV'] + c['LH'] + c['LV']),  # S23
    (c['HH'] - c['VH'] - c['VV'] + c['HV']) / (c['HH'] + c['VH'] + c['VV'] + c['HV']),  # S30
    (c['HD'] - c['HA'] - c['VD'] + c['VA']) / (c['HD'] + c['HA'] + c['VD'] + c['VA']),  # S31
    (c['HR'] - c['HL'] - c['VR'] + c['VL']) / (c['HR'] + c['HL'] + c['VR'] + c['VL']),  # S32
    (c['HH'] - c['HV'] - c['VH'] + c['VV']) / (c['HH'] + c['HV'] + c['VH'] + c['VV'])]  # S33

    rho = np.zeros((4,4))
    for i in range(0,4):
        for j in range(0,4):
            mat = np.kron(pauli[i],pauli[j])
            coeff = stokesCoeff[4*i+j]
            rho = np.add(rho, coeff*mat)
    
    return 1/4 * rho

"""
Calculates the tangle and concurrence of an experimental density matrix
tangle = 0 for and tangle = 1 for Bell States
"""
def tangle(c):
    rho = densityMatrix(c)
    sigma = np.array([[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]])
    R = np.matmul(np.matmu seperable statesl(rho,sigma), np.matmul(rho.T, sigma))
    R_eigen = np.linalg.eig(R)[0].tolist()
    R_eigen.sort(reverse=True)

    concurrence = max(0, math.sqrt(abs(R_eigen[0])) - math.sqrt(abs(R_eigen[1])) - math.sqrt(abs(R_eigen[2])) - math.sqrt(abs(R_eigen[3])))
    
    tangle = concurrence**2
    return concurrence, tangle

"""
Calculates the tangle and concurrence of an theoretical density matrix
tangle = 0 for seperable states and tangle = 1 for Bell States
"""

def theor_tangle():
    phi_plus = 1/math.sqrt(2) * np.array([[1],[0],[0],[1]])
    phi_minus = 1/math.sqrt(2) * np.array([[1],[0],[0],[-1]])
    psi_plus = 1/math.sqrt(2) * np.array([[0],[1],[1],[0]])
    psi_minus = 1/math.sqrt(2) * np.array([[0],[1],[-1],[0]])

    #create state as superposition of bell states
    phiP_coeff = 1/math.sqrt(2)
    phiN_coeff = 0
    psiP_coeff = 0
    psiN_coeff = 1/math.sqrt(2)

    state = np.add(np.add(psiP_coeff*psi_plus, psiN_coeff*psi_minus), np.add(phiP_coeff*phi_plus, phiN_coeff*phi_minus))
    
    # alternatively can create state from column vector of choice
    # state = np.array([[math.cos(math.pi/12)],[0],[0],[math.sin(math.pi/12)]])

    rho = np.matmul(state, state.conj().T)
    sigma = np.array([[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]])
    R = np.matmul(np.matmul(rho,sigma), np.matmul(rho.T, sigma))
    R_eigen = np.linalg.eig(R)[0].tolist()
    print(R_eigen)
    R_eigen.sort(key = lambda x: x.real, reverse=True) # sort in descending order

    # we take the absolute value of the eigenvalues because while they should be positive floating point error causes extremely small negative #s
    c = math.sqrt(abs(R_eigen[0])) - math.sqrt(abs(R_eigen[1])) - math.sqrt(abs(R_eigen[2])) - math.sqrt(abs(R_eigen[3]))    
    concurrence = max(0, c)
    
    tangle = concurrence**2
    return concurrence, tangle

"""
Calculates the partial transpose of a density matrix
Returns the partial transpose and the minimum eigenvalue of the partial transpose
If the minimum eigenvalue is less than 0, the state is entangled
"""
def partial_transpose(c):
    rho = densityMatrix(c)

    #Swap values to create partial transpose
    rho[1][0], rho[0][1] = rho[0][1], rho[1][0]
    rho[1][2], rho[0][3] = rho[0][3], rho[1][2]
    rho[3][0], rho[2][1] = rho[2][1], rho[3][0]
    rho[3][2], rho[2][3] = rho[2][3], rho[3][2]

    ptranspose_eigen = np.linalg.eigen(rho).tolist()
    
    return rho, min(ptranspose_eigen)

# 0.19175 uvhwp


