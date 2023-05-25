# file to compute the maximum k subset of d^2 bell states
# @oscars47

# using sympy to handle symbolic manipulation
from sympy import *
# from sympy.solvers import solve, solveset
from sympy.physics.quantum.dagger import Dagger
# from sympy.printing.mathematica import MCodePrinter
import numpy as np
from itertools import *
import pandas as pd
import time
import signal # limit time for solvers

## Initialize d value ##

# d = int(input('Enter a value for d: '))
d=3
## Choose k ##
# k = int(input('Enter a value for k: '))
k = 4

## Helper Functions for Bell State Generation ##

# generate bell states in number basis
# e.g. |01> for d = 2: [1, 0, 0, 1]
# key: cp (correlation class, phae class). e.g. 12 => c=1, p=2
bs_dict ={}
def generate_bs(d): 
    # store the phase in separate array to make measurement 
    # adapting equation 2 in the 2019
    for c in range(d): # set correlation class
        for p in range(d): # set phase class
            phase = []# stores phase for each join-particle ket
            # ignoring * 1/np.sqrt(d) factor
            numv_ls = [] # number (state) vector
            for j in range(d): # generate qubit
                phase.append(exp((I*2*np.pi*p*j)/d))
                numv = np.zeros(2*d)
                numv[j] = 1 #left qudit: from index 0 -> d-1
                numv[(j+c)%d+d] = 1 # right qudit: from index d -> 2d-1
                numv_ls.append(numv) # add the numv to the overall list
            # we've generated a BS at this point
            bs_dict[str(c)+str(p)]=[numv_ls, phase] # store numv and phase in the dict

# function to make BS more readable
def read_BS(bs):
    print_str = '' # initialize total output string
    for i in range(len(bs[0])):
        numv1 = bs[0][i]
        phase1=bs[1][i]
        i1, = np.where(numv1 == 1)
        print_str+=str(phase1)+'|%i%i> + '%(i1[0], i1[1]-d)
    
    print_str = print_str[:-2] # remove extra + at end
    print(print_str)

## Generate Bell States ##
generate_bs(d)
print('*---------*')
print('initializing with d =', d)
print('k = ', k)
print('num BS:', len(bs_dict))
for key in bs_dict:
    read_BS(bs_dict[key])
print('*---------*')

## Helper functions for measurement ##

# initialize symbols
var_dict={}
alphabet = [] # alphabet of a, b synbols
vbet = [] # alphabet of vs
for i in range(2*d):
    a_i, b_i = Symbol('a'+str(i), real=True), Symbol('b'+str(i), real=True)
    # alphabet['a'+str(i)] = a_i
    # alphabet['b'+str(i)] = b_i
    alphabet.append(a_i)
    alphabet.append(b_i)

    v_i = a_i+b_i*I # split into real and imaginary
    # v_i = Symbol('v'+str(i), complex=True)
    var_dict['v'+str(i)] = v_i
    vbet.append(v_i)

# alphabet=tuple(alphabet)
# get normalization term: sum of modulus squared for each variable
norm_ls = [Dagger(var_dict['v'+str(i)])*var_dict['v'+str(i)] for i in range(len(var_dict))]
norm_ls.append(-1) # append a -1, i.e. sum_i v_iv_i^\dagger -1 = 0
norm_cond = sum(norm_ls)

# for measurement
def measure_BS(bs):
    # print('bs', bs)
    # measured_ls = [] # list to hold sympy matrices which we will take the inner product of with other BS
    measured = Matrix(np.zeros(2*d))
    # go through each joint particle state
    for i, numv in enumerate(bs[0]): # 0th entry holds numv_ls, 1st holds phase
        for j in range(2*d): # check over each index to annihilate
            if numv[j]==1: # found a particle, lower it and append lowered numv to measured ls
                lowered = numv.copy() # need to create copy so we don't annihilate on the original, which we will need as we continue iterating
                lowered[j]-=1
                phase = bs[1][i] # get phase factor
                vj = var_dict['v'+str(j)] # get sympy variable coefficient for this annihilation operator
                # break up phase into re and im; need to deal with really small and should be 0 terms
                phase_re = re(phase)
                phase_im = im(phase)
                # print(phase_re, phase_im)
                if abs(phase_re) < 10**(-4):
                    phase_re=0
                if abs(phase_im) < 10**(-4):
                    phase_im=0
                # print(phase_re, phase_im)
                phase = nsimplify(phase_re) + nsimplify(phase_im)*I
                coef= phase*vj
                # coef = vj
                # print('coef', coef)
                # if N(coef) < 10**(-4):
                #     coef=0
                result = Matrix(lowered)*coef
                measured+=result
            # do nothing if it's not a 1, since then we delete it
            
    return measured

def print_ex():
    print('-----*----')
    print('measuring:')
    bs1 = bs_dict['01'] # pick sample qudit to measure
    bs2 = bs_dict['10'] # pick sample qudit to measure
    print('--bra-ket--')
    read_BS(bs1)
    read_BS(bs2)
    print()
    print('--number--')
    print(bs1)
    print(bs2)
    print()
    print('---measurement:---')
    mbs1 = measure_BS(bs1)
    mbs2 = measure_BS(bs2)
    print('measured bs1', mbs1)
    print('measured bs2', mbs2)
    print()
    print('----inner product mbs1^\dagger * mbs2:----')
    print((Dagger(mbs1)*mbs2)[0])
    print('-----*----')

print_ex()

for bs in bs_dict.values():
    print(bs)

# measure all qudits and store
measured_all = []
for key in bs_dict:
    measured_all.append(measure_BS(bs_dict[key]))

## Find all unique combinations of the d**2 BS choose k ##
# Use Ben's work to find equivalence classes #
# for now, take combinations of k indices from the measured
k_groups = list(combinations(np.arange(0, len(measured_all)), k))

## Take inner product within all unique k groups ##
# takes in k_group and exisiting eqn for the entire k group

# define dataframe to log info about what possible pairs in k group generate solns
# k is the k number, L is left qubit, R is right qubit (in the inner product), and num soln is the number of sets in the sol
# global results
results= pd.DataFrame({'d': [], 'k_group':[], 'num_soln':[]})
def solve_k_eqn(k_group, num_target):
    print('-*----*---*-')
    print('using k group:', k_group)
    pairs_comb = list(combinations(k_group, 2))
    # we want to find 2d unique solutions to cover all the detector modes
    global eqn_re, eqn_im, eqn_total
    eqn_re = [] # list to hold equations which we generate from the inner products
    eqn_im = []
    eqn_total = []
    for pair in pairs_comb:
        inner_prod = Dagger(measured_all[pair[0]])*measured_all[pair[1]]
        
        # either split result into real and imaginary components or keep as complex
        def split_im_re():
            global eqn_re, eqn_im, eqn_total
            re_part= re(inner_prod)[0]
            im_part = im(inner_prod)[0]
            # re_part= nsimplify(re(inner_prod)[0]) # convert to rationals
            # im_part = nsimplify(im(inner_prod)[0])
            if re_part != 0: # want only nonzero terms
                eqn_re.append(re_part)
                eqn_total.append(re_part)
            if im_part != 0:
                eqn_im.append(im_part)
                eqn_total.append(im_part)
        def keep_complex():
            global eqn_total
            eqn_total.append(inner_prod[0])

        split_im_re()
        # keep_complex()

    # eqn_re.append(re(norm_cond))
    # eqn_total.append(re(norm_cond))
    
    # print('eqn re:', eqn_re)
    # print('eqn im:', eqn_im) 
    # output in mathematica and latex languages
    print('eqn total:', mathematica_code(eqn_total), ',', alphabet) 
    print('eqn total:', latex(eqn_total))
    
    ## for timing out ##
    class TimeoutException(Exception):   # Custom exception class
        pass

    def break_after(seconds=2):
        def timeout_handler(signum, frame):   # Custom signal handler
            raise TimeoutException
        def function(function):
            def wrapper(*args, **kwargs):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(seconds)
                try:
                    res = function(*args, **kwargs)
                    signal.alarm(0)      # Clear alarm
                    return res
                except TimeoutException:
                    print('Solve time exceeded :(')
                return
            return wrapper
        return function

    # soln = solve(eqn_total, alphabet, force=True, dict=True)
    # global findsoln
    global results # make df
    global count
    results=pd.DataFrame({'d': [], 'k_group':[], 'num_soln':[]})
    # findsoln=False
    count = 0
    
    # @break_after(60) # 60 second limit per equation
    def try_soln(eqn_total):  
        # global findsoln
        global results
        global count
        # try:
        # print('solving directly')
        # soln_ls = solve(eqn_total, manual=True)

        ## Groebner basis solve ##
        print('finding groebner')
        G_t = groebner(eqn_total, alphabet, order='grlex')
        print(G_t)
        soln_ls= solve(G_t)
        print(soln_ls)

        # soln_ls = solve(eqn_total, manual=True)


        # soln_ls = solve_poly_system(eqn_total)
        # soln_ls = solve_triangulated(eqn_total)
        # print(soln_ls)
        # print(len(soln))
        # find all real parts of solution
        # re_soln = []
        # for soln in soln_ls:
        #     # get keys
        #     values = list(soln.values())
        #     # print(values)
        #     found_im = False
        #     all_zero=False
        #     if values== list(np.zeros(len(values))):
        #         # print('trivial solution, not including')
        #         all_zero=True
        #     for value in values:
        #         if im(value) != 0: # found imaginary value
        #             print('found imaginary solution, not including', value)
        #             found_im = True
        #     if (found_im==False) and (all_zero==False):
        #         re_soln.append(soln)
        if len(soln_ls)>0:
            print('found a solution!', soln_ls)
            results = results.append({'d': d, 'k_group':k_group, 'num_soln':len(soln_ls)}, ignore_index=True)
            # findsoln = True # found a solution!
            count+=len(soln_ls)
        # except:
        #     print('there was a problem with the solve')
            # ValueError: Absolute values cannot be inverted in the complex domain.

        # soln = nonlinsolve(eqn_total, alphabet)
        # soln = solve(eqn_total, alphabet, manual=True, dict=True)
        # # soln = solve(eqn_total, alphabet, check=False, rational=True, manual=True, set=True, implicit=True)

        # # soln = nsolve(eqn_total, alphabet, np.zeros(len(alphabet))) # need as many equations as variables for nsolve
        # print('soln:', soln)
        # if len(soln) > 0 and len(soln[1])>2:
        #     # print(len(soln[1]))
        #     results = {'d': d, 'k_group':k_group, 'num_soln':len(soln[1])}
        #     findsoln = True # found a solution!
    
    ## idea: we can take advantage of the undertermined nature of the system to substitute in lots of 0s and 1s ##
    def simplify(eqn_total, sub_vec, n, num_target): # num_target is how many solutions minimum we want to find
        # get all unique permutations
        perm_sub = list(set(permutations(sub_vec, n)))
        # combinations of variables
        alpha_comb = list(combinations(alphabet, n))
        # build substitution dictionary
        for perm in perm_sub: # do this for each possible unique permutation of substitution vectors
            for var_group in alpha_comb: # check each combination of variables 
                sub_dict = {}
                for i, var in enumerate(var_group): # assign variables
                    sub_dict[var]=perm[i]

                eqn_sim = [] # build simplified system to solve
                for exp in eqn_total:
                    eqn_sim.append(exp.subs(sub_dict))

                # now try to solve
                # print('trying simplified eqn:', eqn_sim)
                try_soln(eqn_sim)
                # if count== True: # did find >= 1 solution:
                #     print('found a solution for k=%i!'%k)
                #     print('solution:', eqn_re)
                    # print(findsoln)
                    # print(results)
                    # return findsoln, results
                if count>=num_target:
                    print(results)
                    return True
            
        return False
        # return findsoln, results
    try_soln(eqn_total)

    # num free vars
    # num_free = int(4*d - ((k-1)*k)/2) # lower bound
    # for n in range(num_free, 4*d, 1): # number of free variables
    #     # get combinations of 0s and 1s
    #     for p in range(n): # how many 1s to include
    #         start = np.zeros(n) # start with 0s
    #         if p > 0:
    #             for l in range(p):
    #                 start[l]=1
    #         done = simplify(eqn_total, start, n, num_target)
    #         if done==True:
    #             break
    #     if done==True:
    #         break
   
## set num target solutions
num_target = 1 # for now, get >= 1 soln


## to do:
#  need to implement finding 2d-1 other orthogonal ones
# check  solving full equation for 15 secs first?
# parallize!!!!

def do_k_computation():
    # log computation time
    start_time = time.time()
    for k_group in k_groups:
        solve_k_eqn(k_group, num_target)
        # if not(isinstance(results, int)):
        #     results = results.append(results, ignore_index=True)
        if count>=num_target:
            break
    end_time = time.time()
    # print(results)
    results.to_csv('d=%i,k=%i_results.csv'%(d, k))
    print('computation took %s seconds'%(end_time-start_time))

do_k_computation()