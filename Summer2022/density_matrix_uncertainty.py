import numpy as np
import pandas as pd
import math
import scipy.optimize as spo
from compile_measurements import *

# Dealing with uncertainty
from uncertainties import ufloat, unumpy
from uncertainties.umath import *

"""
returns density matrix rho with uncertainties in each entry
c is the dictionary of c4_averages and c_un is the dictionary of c4 uncertainties
"""
def densityMatrix_and_uncertainty(c, c_un, save=False):
    # Four Pauli matrices
    sig0 = np.array([[1,0],[0,1]])
    sig1 = np.array([[0,1],[1,0]])
    sig2 = np.array([[0,-1j],[1j,0]])
    sig3 = np.array([[1,0],[0,-1]])
    pauli = [sig0] + [sig1] + [sig2] + [sig3]

    DD = ufloat(c['DD'], c_un['DD'])
    DA = ufloat(c['DA'], c_un['DA'])
    AD = ufloat(c['AD'], c_un['AD'])
    AA = ufloat(c['AA'], c_un['AA'])

    RR = ufloat(c['RR'], c_un['RR'])
    RL = ufloat(c['RL'], c_un['RL'])
    LR = ufloat(c['LR'], c_un['LR'])
    LL = ufloat(c['LL'], c_un['LL'])

    HH = ufloat(c['HH'], c_un['HH'])
    HV = ufloat(c['HV'], c_un['HV'])
    VH = ufloat(c['VH'], c_un['VH'])
    VV = ufloat(c['VV'], c_un['VV'])

    DR = ufloat(c['DR'], c_un['DR'])
    DL = ufloat(c['DL'], c_un['DL'])
    AR = ufloat(c['AR'], c_un['AR'])
    AL = ufloat(c['AL'], c_un['AL'])

    DH = ufloat(c['DH'], c_un['DH'])
    DV = ufloat(c['DV'], c_un['DV'])
    AH = ufloat(c['AH'], c_un['AH'])
    AV = ufloat(c['AV'], c_un['AV'])

    RD = ufloat(c['RD'], c_un['RD'])
    RA = ufloat(c['RA'], c_un['RA'])
    LD = ufloat(c['LD'], c_un['LD'])
    LA = ufloat(c['LA'], c_un['LA'])

    RH = ufloat(c['RH'], c_un['RH'])
    RV = ufloat(c['RV'], c_un['RV'])
    LH = ufloat(c['LH'], c_un['LH'])
    LV = ufloat(c['LV'], c_un['LV'])

    HD = ufloat(c['HD'], c_un['HD'])
    HA = ufloat(c['HA'], c_un['HA'])
    VD = ufloat(c['VD'], c_un['VD'])
    VA = ufloat(c['VA'], c_un['VA'])

    HR = ufloat(c['HR'], c_un['HR'])
    HL = ufloat(c['HL'], c_un['HL'])
    VR = ufloat(c['VR'], c_un['VR'])
    VL = ufloat(c['VL'], c_un['VL'])

    stokesCoeff = [ufloat(1,0), # S00
    (DD-DA-AA+AD)/(DD+DA+AA+AD), #S01
    (RR+LR-LL-RL)/(RR+LR+LL+RL), #S02
    (HH-HV-VV+VH)/(HH+HV+VV+VH), #S03
    (DD-AD-AA+DA)/(DD+AD+AA+DA), #S10
    (DD-DA-AD+AA)/(DD+DA+AD+AA), #S11
    (DR-DL-AR+AL)/(DR+DL+AR+AL), #S12
    (DH-DV-AH+AV)/(DH+DV+AH+AV), #S13
    (RR+RL-LL-LR)/(RR+RL+LL+LR), #S20
    (RD-RA-LD+LA)/(RD+RA+LD+LA), #S21
    (RR-RL-LR+LL)/(RR+RL+LR+LL), #S22
    (RH-RV-LH+LV)/(RH+RV+LH+LV), #S23
    (HH-VH-VV+HV)/(HH+VH+VV+HV), #S30
    (HD-HA-VD+VA)/(HD+HA+VD+VA), #S31
    (HR-HL-VR+VL)/(HR+HL+VR+VL), #S32
    (HH-HV-VH+VV)/(HH+HV+VH+VV)  #S33
    ]

    rho = np.zeros((4,4))
    rho_un = np.zeros((4,4))
    for i in range(0,4):
        for j in range(0,4):
            mat = np.kron(pauli[i],pauli[j])
            coeff = stokesCoeff[4*i+j]
            coeff_uncertainty = coeff.std_dev
            coeff = coeff.nominal_value
            full_mat = coeff*mat
            full_mat_uncertainty = coeff_uncertainty*mat
            rho = np.add(rho, full_mat)
            rho_un = np.add(rho_un, full_mat_uncertainty)
    
    rho *= 1/4
    rho_un *= 1/4

    print("average uncertainty", np.average(rho_un), '\n')
    print("max uncertainty", np.amax(rho_un), '\n')

    if save:
        name = input("Enter name of density matrix file (don't include .csv):")

        row0 = [rho[0][0], rho_un[0][0], rho[0][1], rho_un[0][1], rho[0][2], rho_un[0][2], rho[0][3], rho_un[0][3]]
        row1 = [rho[1][0], rho_un[1][0], rho[1][1], rho_un[1][1], rho[1][2], rho_un[1][2], rho[1][3], rho_un[1][3]]
        row2 = [rho[2][0], rho_un[2][0], rho[2][1], rho_un[2][1], rho[2][2], rho_un[2][2], rho[2][3], rho_un[2][3]]
        row3 = [rho[3][0], rho_un[3][0], rho[3][1], rho_un[3][1], rho[3][2], rho_un[3][2], rho[3][3], rho_un[3][3]]

        rows = [row0, row1, row2, row3]
        name = name +"__rho.csv"
        df = pd.DataFrame(rows, columns = ['row[0]', '+- row[0] uncertainty', 
                'row[1]', '+- row[1] uncertainty', 'row[2]', '+- row[2] uncertainty', 'row[3]', '+- row[3] uncertainty'])
        df.to_csv(name, index=False)

    return rho, rho_un
