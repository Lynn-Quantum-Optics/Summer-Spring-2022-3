"""
Calculates the Witness States
Based on Yilin Li's Code
Authors: Eritas, Ben, Becca
"""

import math
import scipy.optimize as spo
import pandas as pd
from compile_measurements import *
from datetime import datetime
from witness_helper import *

"""
CalculateW calculates the witness values of the given data
c4 is a dictionary of coincidence counts with format {basis:c4 average}
ExpType is based on Experiments Automated
date is the date that the measurement occured, default is the time the command is run
creates a csv file containing the witness values and the optimized a and b if exportCSV is True
returns an list of the witnesse values and optimized a and b 
"""
def calculateW(c4, ExpType, c4_un = {}, getUncertainty = False, exportCSV = False, date = datetime.now().strftime("%m/%d/%Y__%H:%M:%S")):
    # p_ij are the tensor products of the Pauli Matrices
    p_xx= p_yy= p_zz= p_xI= p_Ix= p_yI= p_Iy= p_zI= p_Iz= p_xy= p_yx= p_yz= p_zy= p_xz= p_zx = 0
    if ExpType == "Full Tomography":
        p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_xy, p_yx, p_yz, p_zy, p_xz, p_zx = getStokesParameters(c4, c4_un, ExpType, getUncertainty)
    elif ExpType == "Witness":
        p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz = getStokesParameters(c4, c4_un, ExpType, getUncertainty)
    elif ExpType == "W1 prime to W3 prime":
        p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_xy, p_yx = getStokesParameters(c4, c4_un, ExpType, getUncertainty)
    elif ExpType == "W4 prime to W6 prime":
        p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_yz, p_zy = getStokesParameters(c4, c4_un, ExpType, getUncertainty)
    elif ExpType == "W7 prime to W9 prime":
        p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_xz, p_zx = getStokesParameters(c4, c4_un, ExpType, getUncertainty)

    p_un_list = [0]*15
    p_list = [p_xx, p_yy, p_zz, p_xI, p_Ix, p_yI, p_Iy, p_zI, p_Iz, p_xy, p_yx, p_yz, p_zy, p_xz, p_zx]
    if getUncertainty: 
        p_list = [x if isinstance(x, int) or isinstance(x, float) else x.nominal_value for x in p_list]
        p_un_list = [x if isinstance(x, int) or isinstance(x, float) else x.std_dev for x in p_list]
    
    #//////////////////////////////////Original 6 Witness///////////////////////////////////////
    def EntanglementWitnessOne(t):
        W1 = 1/4*(1 + p_zz + ((math.cos(t))**2 - (math.sin(t))**2)*p_xx 
                    + ((math.cos(t))**2 - (math.sin(t))**2)*p_yy
                    + 2*math.sin(t)*math.cos(t)*(p_zI + p_Iz))
        return W1

    def EntanglementWitnessTwo(t):
        W2 = 1/4*(1 - p_zz  + ((math.cos(t))**2 - (math.sin(t))**2)*p_xx 
                    - ((math.cos(t))**2 - (math.sin(t))**2)*p_yy
                    + 2*math.sin(t)*math.cos(t)*(p_zI - p_Iz))
        return W2

    def EntanglementWitnessThree(t):
        W3 = 1/4*(1 + p_xx + ((math.cos(t))**2 - (math.sin(t))**2)*p_zz 
                    + ((math.cos(t))**2 - (math.sin(t))**2)*p_yy
                    + 2*math.sin(t)*math.cos(t)*(p_xI + p_Ix))
        return W3

    def EntanglementWitnessFour(t):
        W4 = 1/4*(1 - p_xx + ((math.cos(t))**2 - (math.sin(t))**2)*p_zz 
                    - ((math.cos(t))**2 - (math.sin(t))**2)*p_yy
                    - 2*math.sin(t)*math.cos(t)*(p_xI - p_Ix))
        return W4

    def EntanglementWitnessFive(t):
        W5 = 1/4*(1 + p_yy + ((math.cos(t))**2 - (math.sin(t))**2)*p_zz 
                    + ((math.cos(t))**2 - (math.sin(t))**2)*p_xx
                    + 2*math.sin(t)*math.cos(t)*(p_yI + p_Iy))
        return W5

    def EntanglementWitnessSix(t):
        W6 = 1/4*(1 - p_yy + ((math.cos(t))**2 - (math.sin(t))**2)*p_zz 
                    - ((math.cos(t))**2 - (math.sin(t))**2)*p_xx
                    - 2*math.sin(t)*math.cos(t)*(p_yI - p_Iy))        
        return W6
    
    #//////////////////////////////////New 9 Prime Witnesses///////////////////////////////////////
    
    #//////////////////////////////////Triplet 1: require p_xy and p_yx as well///////////////////////////////////////
    def EntanglementWitness1p(x):
        t = x[0]
        a = x[1]
        W1p = 1/4*(1 + p_zz + math.cos(2*t)*(p_xx + p_yy)
              + math.sin(2*t)*math.cos(a)*(p_zI + p_Iz)
              + math.sin(2*t)*math.sin(a)*(p_xy - p_yx))
        return W1p
    
    def EntanglementWitness2p(x):
        t = x[0]
        a = x[1]
        W2p = 1/4*(1 - p_zz + math.cos(2*t)*(p_xx - p_yy)
              + math.sin(2*t)*math.cos(a)*(p_zI - p_Iz)
              - math.sin(2*t)*math.sin(a)*(p_xy + p_yx))
        return W2p
    
    def EntanglementWitness3p(x):
        t = x[0]
        a = x[1]
        b = x[2]
        W3p = 1/4*(((math.cos(t))**2)*(1 + p_zz)
              + ((math.sin(t))**2)*(1 - p_zz)
              + ((math.cos(t))**2)*math.cos(b)*(p_xx + p_yy)
              + ((math.sin(t))**2)*math.cos(2*a -b)*(p_xx - p_yy)
              + math.sin(2*t)*math.cos(a)*p_xI
              + math.sin(2*t)*math.cos(a-b)*p_Ix
              + math.sin(2*t)*math.sin(a)*p_yI
              + math.sin(2*t)*math.sin(a-b)*p_Iy
              + ((math.cos(t))**2)*math.sin(b)*(p_yx - p_xy)
              + ((math.sin(t))**2)*math.sin(2*a-b)*(p_yx + p_xy))
        return W3p
    
    #//////////////////////////////////Triplet 2: require p_yz and p_zy as well///////////////////////////////////////
    def EntanglementWitness4p(x):
        t = x[0]
        a = x[1]
        W4p = 1/4*(1 + p_xx + math.cos(2*t)*(p_zz + p_yy)
              + math.sin(2*t)*math.cos(a)*(p_Ix + p_xI)
              + math.sin(2*t)*math.sin(a)*(p_yz - p_zy))
        return W4p
    
    def EntanglementWitness5p(x):
        t = x[0]
        a = x[1]
        W5p = 1/4*(1 - p_xx + math.cos(2*t)*(p_zz - p_yy)
              + math.sin(2*t)*math.cos(a)*(p_Ix - p_xI)
              - math.sin(2*t)*math.sin(a)*(p_yz + p_zy))
        return W5p
    
    def EntanglementWitness6p(x):
        t = x[0]
        a = x[1]
        b = x[2]
        W6p = 1/4*(((math.cos(t))**2)*((math.cos(a))**2)*(1 + p_zz + p_zI + p_Iz)
              + ((math.cos(t))**2)*((math.sin(a))**2)*(1 - p_zz + p_zI - p_Iz)
              + ((math.sin(t))**2)*((math.cos(b))**2)*(1 + p_zz - p_zI - p_Iz)
              + ((math.sin(t))**2)*((math.sin(b))**2)*(1 - p_zz - p_zI + p_Iz)
              + math.sin(2*t)*math.cos(a)*math.cos(b)*(p_xx + p_yy)
              + math.sin(2*t)*math.sin(a)*math.sin(b)*(p_xx - p_yy)
              + math.sin(2*t)*math.cos(a)*math.sin(b)*(p_yz + p_yI)
              + math.sin(2*t)*math.sin(a)*math.cos(b)*(p_yz - p_yI)
              - ((math.cos(t))**2)*math.sin(2*a)*(p_zy + p_Iy)
              - ((math.sin(t))**2)*math.sin(2*b)*(p_zy - p_Iy))
        return W6p
    
    

    #//////////////////////////////////Triplet 3: require p_xz and p_zx as well///////////////////////////////////////
    def EntanglementWitness7p(x):
        t = x[0]
        a = x[1]
        W7p = 1/4*(1 + p_yy + math.cos(2*t)*(p_zz + p_xx)
              + math.sin(2*t)*math.cos(a)*(p_zx - p_xz)
              - math.sin(2*t)*math.sin(a)*(p_yI + p_Iy))
        return W7p
    
    def EntanglementWitness8p(x):
        t = x[0]
        a = x[1]
        W8p = 1/4*(1 - p_yy + math.cos(2*t)*(p_zz - p_xx)
              + math.sin(2*t)*math.cos(a)*(p_zx + p_xz)
              + math.sin(2*t)*math.sin(a)*(p_yI - p_Iy))
        return W8p
    
    def EntanglementWitness9p(x):
        t = x[0]
        a = x[1]
        b = x[2]
        W9p = 1/4*(((math.cos(t))**2)*((math.cos(a))**2)*(1 + p_zz + p_zI + p_Iz)
              + ((math.cos(t))**2)*((math.sin(a))**2)*(1 - p_zz + p_zI - p_Iz)
              + ((math.sin(t))**2)*((math.cos(b))**2)*(1 + p_zz - p_zI - p_Iz)
              + ((math.sin(t))**2)*((math.sin(b))**2)*(1 - p_zz - p_zI + p_Iz)
              + math.sin(2*t)*math.cos(a)*math.cos(b)*(p_xx + p_yy)
              + math.sin(2*t)*math.sin(a)*math.sin(b)*(p_xx - p_yy)
              + ((math.cos(t))**2)*math.sin(2*a)*(p_Ix + p_zx)
              + ((math.sin(t))**2)*math.sin(2*b)*(p_Ix - p_zx)
              + math.sin(2*t)*math.cos(a)*math.sin(b)*(p_xI + p_xz)
              + math.sin(2*t)*math.sin(a)*math.cos(b)*(p_xI - p_xz))
        return W9p
    
    #////////////////////////////////// To Get Max Value Original 6 Witness///////////////////////////////////////
    def n_EntanglementWitnessOne(t):
        W1 = 1/4*(1 + p_zz + ((math.cos(t))**2 - (math.sin(t))**2)*p_xx 
                    + ((math.cos(t))**2 - (math.sin(t))**2)*p_yy
                    + 2*math.sin(t)*math.cos(t)*(p_zI + p_Iz))
        return -W1

    def n_EntanglementWitnessTwo(t):
        W2 = 1/4*(1 - p_zz  + ((math.cos(t))**2 - (math.sin(t))**2)*p_xx 
                    - ((math.cos(t))**2 - (math.sin(t))**2)*p_yy
                    + 2*math.sin(t)*math.cos(t)*(p_zI - p_Iz))
        return -W2

    def n_EntanglementWitnessThree(t):
        W3 = 1/4*(1 + p_xx + ((math.cos(t))**2 - (math.sin(t))**2)*p_zz 
                    + ((math.cos(t))**2 - (math.sin(t))**2)*p_yy
                    + 2*math.sin(t)*math.cos(t)*(p_xI + p_Ix))
        return -W3

    def n_EntanglementWitnessFour(t):
        W4 = 1/4*(1 - p_xx + ((math.cos(t))**2 - (math.sin(t))**2)*p_zz 
                    - ((math.cos(t))**2 - (math.sin(t))**2)*p_yy
                    - 2*math.sin(t)*math.cos(t)*(p_xI - p_Ix))
        return -W4

    def n_EntanglementWitnessFive(t):
        W5 = 1/4*(1 + p_yy + ((math.cos(t))**2 - (math.sin(t))**2)*p_zz 
                    + ((math.cos(t))**2 - (math.sin(t))**2)*p_xx
                    + 2*math.sin(t)*math.cos(t)*(p_yI + p_Iy))
        return -W5

    def n_EntanglementWitnessSix(t):
        W6 = 1/4*(1 - p_yy + ((math.cos(t))**2 - (math.sin(t))**2)*p_zz 
                    - ((math.cos(t))**2 - (math.sin(t))**2)*p_xx
                    - 2*math.sin(t)*math.cos(t)*(p_yI - p_Iy))        
        return -W6


    def findMinW():
        if ExpType == "Full Tomography":
            W1 = ["W1"] + optimizeW(EntanglementWitnessOne, W1_uncertainty, p_un_list)
            W2 = ["W2"] + optimizeW(EntanglementWitnessTwo, W2_uncertainty, p_un_list)
            W3 = ["W3"] + optimizeW(EntanglementWitnessThree, W3_uncertainty, p_un_list)
            W4 = ["W4"] + optimizeW(EntanglementWitnessFour, W4_uncertainty, p_un_list)
            W5 = ["W5"] + optimizeW(EntanglementWitnessFive, W5_uncertainty, p_un_list)
            W6 = ["W6"] + optimizeW(EntanglementWitnessSix, W6_uncertainty, p_un_list)
            W1p = ["W1p"] + optimizeW_2p(EntanglementWitness1p, W1p_uncertainty, p_un_list)
            W2p = ["W2p"] + optimizeW_2p(EntanglementWitness2p, W2p_uncertainty, p_un_list)
            W3p = ["W3p"] + optimizeW_3p(EntanglementWitness3p, W3p_uncertainty, p_un_list)
            W4p = ["W4p"] + optimizeW_2p(EntanglementWitness4p, W4p_uncertainty, p_un_list)
            W5p = ["W5p"] + optimizeW_2p(EntanglementWitness5p, W5p_uncertainty, p_un_list)
            W6p = ["W6p"] + optimizeW_3p(EntanglementWitness6p, W6p_uncertainty, p_un_list)
            W7p = ["W7p"] + optimizeW_2p(EntanglementWitness7p, W7p_uncertainty, p_un_list)
            W8p = ["W8p"] + optimizeW_2p(EntanglementWitness8p, W8p_uncertainty, p_un_list)
            W9p = ["W9p"] + optimizeW_3p(EntanglementWitness9p, W9p_uncertainty, p_un_list)
            W_list = [W1, W2, W3, W4, W5, W6, W1p, W2p, W3p, W4p, W5p, W6p, W7p, W8p, W9p]
            return W_list
        elif ExpType == "Witness":
            W1 = ["W1 min"] + optimizeW(EntanglementWitnessOne, W1_uncertainty, p_un_list)
            W1_m = ["W1 max"] + maxW(n_EntanglementWitnessOne, W1_uncertainty, p_un_list)
            W2 = ["W2 min"] + optimizeW(EntanglementWitnessTwo, W2_uncertainty, p_un_list)
            W2_m = ["W2 max"] + maxW(n_EntanglementWitnessTwo, W2_uncertainty, p_un_list)
            W3 = ["W3 min"] + optimizeW(EntanglementWitnessThree, W3_uncertainty, p_un_list)
            W3_m = ["W3 max"] + maxW(n_EntanglementWitnessThree, W3_uncertainty, p_un_list)
            W4 = ["W4 min"] + optimizeW(EntanglementWitnessFour, W4_uncertainty, p_un_list)
            W4_m = ["W4 max"] + maxW(n_EntanglementWitnessFour, W4_uncertainty, p_un_list)
            W5 = ["W5 min"] + optimizeW(EntanglementWitnessFive, W5_uncertainty, p_un_list)
            W5_m = ["W5 max"] + maxW(n_EntanglementWitnessFive, W5_uncertainty, p_un_list)
            W6 = ["W6 min"] + optimizeW(EntanglementWitnessSix, W6_uncertainty, p_un_list)
            W6_m = ["W6 max"] + maxW(n_EntanglementWitnessSix, W6_uncertainty, p_un_list)
            W_list = [W1, W1_m, W2, W2_m, W3, W3_m, W4, W4_m, W5, W5_m, W6, W6_m]
            return W_list
        elif ExpType == "W1 prime to W3 prime":
            W1p = ["W1p"] + optimizeW_2p(EntanglementWitness1p, W1p_uncertainty, p_un_list)
            W2p = ["W2p"] + optimizeW_2p(EntanglementWitness2p, W2p_uncertainty, p_un_list)
            W3p = ["W3p"] + optimizeW_3p(EntanglementWitness3p, W3p_uncertainty, p_un_list)
            W_list = [W1p, W2p, W3p]
            return W_list
        elif ExpType == "W4 prime to W6 prime":
            W4p = ["W4p"] + optimizeW_2p(EntanglementWitness4p, W4p_uncertainty, p_un_list)
            W5p = ["W5p"] + optimizeW_2p(EntanglementWitness5p, W5p_uncertainty, p_un_list)
            W6p = ["W6p"] + optimizeW_3p(EntanglementWitness6p, W6p_uncertainty, p_un_list)
            W_list = [W4p, W5p, W6p]
            return W_list
        elif ExpType == "W7 prime to W9 prime":
            W7p = ["W7p"] + optimizeW_2p(EntanglementWitness7p, W7p_uncertainty, p_un_list)
            W8p = ["W8p"] + optimizeW_2p(EntanglementWitness8p, W8p_uncertainty, p_un_list)
            W9p = ["W9p"] + optimizeW_3p(EntanglementWitness9p, W9p_uncertainty, p_un_list)
            W_list = [W7p, W8p, W9p]
            return W_list
    
    W_info = findMinW()
    if ExpType != "Witness":
        W_info.sort(key= lambda x: x[1])
    else:
        W_val = [x[1] for x in W_info]
        print('\n\n\n\n\n\nWitness Values\n')
        print(W_val)
        print('\n\n\n\n\n\n')
    
    # export as csv file
    if exportCSV:
        df = pd.DataFrame(W_info, columns = ['Witness State', 'value', 'optimized theta', 'optimized alpha', 'optimized betta'])
        name = date + '__Witness_values.csv'
        df.to_csv(name, index=False)
        print("Created Witness calculations file with name: ", name)
    return W_info