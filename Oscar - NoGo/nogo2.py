# file to generate systems for maximal distinguishability using my matrix notation
# @oscar47

import numpy as np
from sympy import *
from sympy.physics.quantum.dagger import Dagger

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
    # helper f function
    def f(x):
        rp = re(x)
        ip = im(x)
        if rp==0 and ip==0:
            return 0
        else:
            return 1

    def get_Sdj(c,p, j):
        Sdj = np.zeros((2*d,1))
        Sdj[j,0] = 1
        Sdj[d+(d+j-c) % d,0] = 1
        phase = ((2*np.pi* p)  * ((d+j-c) % d))/ d
        # print(2*np.pi* p, ((d+j-c) % d), (2*np.pi* p)  * ((d+j-c) % d), phase)
        Sdj = Sdj * exp(phase* I )
        # resize to be column vectors
        Sdj.resize(2*d, 1)
        return Sdj

    # define c and p
    c1, p1 = cp1[0], cp1[1]
    c2, p2 = cp2[0], cp2[1]

    # define our j1 and j2 indices
    j1_ls = np.arange(0, d, 1)
    j2_ls = np.arange(0, d, 1)

    eqn_ls = [] # variable to hold the system

    for j1 in j1_ls:
        # create jth index Bell for 1st
        Sdj1 = get_Sdj(c1,p1, j1)

        for j2 in j2_ls:
            Sdj2 = get_Sdj(c2,p2, j2)

            # get lj lists
            lj1_ls = [j1, d+ ((d+j1-c1) % d)]
            lj2_ls = [j2, d + ((d+j2-c2) % d)]

            for lj1 in lj1_ls:
                for lj2 in lj2_ls:
                    if f(Sdj1[lj1,0]*Sdj2[lj2,0]) > 0:
                        # print(N(Sdj1[lj1,0]), N(Sdj2[lj2,0]))
                        # if not 0, apply measurement
                        # print(lj1, lj2)
                        Md = eye(2*d)
                        Md[lj1, lj1]=0
                        Md[lj2, lj2]=0
                        # print((conjugate(var_dict['v'+str(lj1)])*var_dict['v'+str(lj2)]*Dagger(Sdj1)*Md*Sdj2)[0])
                        eqn_ls.append((conjugate(var_dict['v'+str(lj1)])*var_dict['v'+str(lj2)]*Dagger(Sdj1)*Md*Sdj2)[0])
   
    eqn= sum(eqn_ls)
    print(eqn)
    return eqn

measure_pair((1,1), (0,1))
