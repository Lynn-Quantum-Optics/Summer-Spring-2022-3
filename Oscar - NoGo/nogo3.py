# file to compute inner products on bell states, using 4/15/23 expression
# @oscar47

import numpy as np
from sympy import *
from sympy.physics.quantum.dagger import Dagger
from itertools import *

## set d and k values ##
d = 3
k = 3

# initialize symbols
var_dict={}
vbet = [] # alphabet of vs
for i in range(2*d):
    v_i = Symbol('v'+str(i), complex=True)
    var_dict['v'+str(i)] = v_i
    vbet.append(v_i)

def measure_pair(cp1, cp2):
    # define c and p
    c1, p1 = cp1[0], cp1[1]
    c2, p2 = cp2[0], cp2[1]

    # define our j1 and j2 indices
    j1_ls = np.arange(0, d, 1)
    j2_ls = np.arange(0, d, 1)

    eqn_ls = [] # variable to hold the system

    if c1 == c2:
        for j in np.arange(0, 2*d, 1):
            gamma = d + ((d + j - c1) % d)
            phase = exp((2*pi * I* gamma)/d *(p2-p1))
            term = phase*Dagger(var_dict['v'+str(j)])*var_dict['v'+str(j)]
            eqn_ls.append(term)

    else:
        for j1 in j1_ls:
            for j2 in j2_ls:
                gamma1 = d + ((d + j1 - c1) % d)
                gamma2 = d + ((d + j2 - c2) % d)
                if ((j1!=j2) and (c1 != c2)) or ((c1 == c2) and (j1 == j2)):
                    lambda1 = j1
                    lambda2 = j2
                elif (j1==j2):
                    lambda1 = gamma1
                    lambda2 = gamma2
                phase = exp((2*pi * I)/d* (p2*gamma2 - p1*gamma1))
                term = phase*Dagger(var_dict['v'+str(lambda1)])*var_dict['v'+str(lambda2)]
                eqn_ls.append(term)

    eqn= sum(eqn_ls)
    def print_info(): # function to print out individual equations
        print(cp1, cp2)
        # print(latex(eqn))
        print(eqn)
        print('------')
    # print_info()
    return eqn

## testing sample states ##
# eqn = measure_pair((0,0), (0,1))
# eqn = measure_pair((1,1), (0,1))
# eqn = measure_pair((0,0), (1,1))


## for given k, figure out how many combinations ##
def build_cp():
    cp_ls = []
    for c in range(d):
        for p in range(d):
            cp_ls.append((c, p))
    return cp_ls
cp_ls= build_cp()
k_cp = list(combinations(cp_ls, k))

## perform measurements of d^2 choose k choose 2 pairs ##
def measure_group(k_cp):
    for kg in k_cp:
        # have to get all combinations of pairs
        k_pair = list(combinations(kg, 2))
        eqn_master= []
        print('For the $k=' + str(k) + '$ group $' + str(kg) +'$,')
        print('\\begin{equation}')
        print('\\begin{split}')
        for pair in k_pair:
            eqn = measure_pair(pair[0], pair[1])
            print(latex(eqn), " &= 0 \\\\")
            eqn_master.append(eqn)
        print('\\end{split}')
        print('\\end{equation}')
        ## do solve on eqn system ##

measure_group(k_cp)    