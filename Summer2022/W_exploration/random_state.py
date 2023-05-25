"""
Code based on 2021 Jan Roik, Karol Bartkiewicz et. all's source code from the paper 
"Accuracy of Entanglement Detection via Artificial Neural Networks and Human-Designed Entanglement Witnesses"
"""

import random
import decimal
import numpy as np
import math
from W_helper_file import*
from sympy import Matrix, trigsimp, Trace
import sympy as sym

pi = math.pi
e = math.e

"""
returns the matrix M referenced in the Appendix of Roik et al's 2021 paper
"""
def create_M():
    # create random unit simplex
    # method based on
    # https://cs.stackexchange.com/questions/3227/uniform-sampling-from-a-simplex
    l = [np.random.rand(), np.random.rand(), np.random.rand()]
    l = l.sort()
    r_1 = l[0] 
    r_2 = l[1] - l[0]
    r_3 = l[2] - l[1]
    r_4 = 1 - l[2]

    trace = r_1 + r_2 + r_3 + r_4

    if round(trace, 5) == 0:
        print('retrying create_M to create M with nonzero trace')
        create_M()
    else:
        M = np.array([[r_1/trace, 0, 0, 0], 
                      [0, r_2/trace, 0, 0], 
                      [0, 0, r_3/trace, 0], 
                      [0, 0, 0, r_4/trace]])
        
        trace = round(np.trace(M), 5)
        assert trace == 1, 'trace of M is not 1'
        return M

"""
creates a random 2x2 submatrix in order to create u_j
"""
def create_uj_sub():
    alpha_j = pi*random.uniform(0.000, 2.000)
    psi_j = pi*random.uniform(0.000, 2.000)
    ksi_j = pi*random.uniform(0.000, 2.000)
    epsilon_j = random.uniform(0.000, 1.000)
    phi_j = math.asin(math.sqrt(epsilon_j))

    # Basic u_j matrix
    u_j_00 = (e**(1j*alpha_j))*(e**(1j*psi_j))*math.cos(phi_j)
    u_j_01 = (e**(1j*alpha_j))*(e**(1j*ksi_j))*math.sin(phi_j)
    u_j_10 = -(e**(1j*alpha_j))*(e**(-1j*ksi_j))*math.sin(phi_j)
    u_j_11 = (e**(1j*alpha_j))*(e**(-1j*psi_j))*math.cos(phi_j)
    
    return u_j_00, u_j_01, u_j_10, u_j_11

"""
returns the matrix U described in the Appendix of Roik et al's 2021 paper
"""
def create_U():
    u_1 = np.identity(4, dtype = complex)
    u_1[2][2], u_1[2][3], u_1[3][2], u_1[3][3] = create_uj_sub()

    u_2 = np.identity(4, dtype = complex)
    u_2[1][1], u_2[1][2], u_2[2][1], u_2[2][2] = create_uj_sub()
    
    u_3 = np.identity(4, dtype = complex)
    u_3[0][0], u_3[0][1], u_3[1][0], u_3[1][1] = create_uj_sub()
    
    u_4 = np.identity(4, dtype = complex)
    u_4[2][2], u_4[2][3], u_4[3][2], u_4[3][3] = create_uj_sub()

    u_5 = np.identity(4, dtype = complex)
    u_5[1][1], u_5[1][2], u_5[2][1], u_5[2][2] = create_uj_sub()
    
    u_6 = np.identity(4, dtype = complex)
    u_6[2][2], u_6[2][3], u_6[3][2], u_6[3][3] = create_uj_sub()
    
    U = u_1 @ u_2 @ u_3 @ u_4 @ u_5 @ u_6
    return U

"""
Returns the density matrix of a random 2 qubit quantum state
"""
def create_random_rho():
    U = create_U()
    U_hermitian = U.transpose().conjugate()

    M = create_M()
    random_density_matrix = (U @ M @ U_hermitian).round(10)
    trace = round(np.trace(random_density_matrix), 5)
    purity = round(np.trace(random_density_matrix @ random_density_matrix), 5)

    assert purity >= 0.25, "Purity of Density Matrix must be greater than 0.25"
    assert trace == 1, "Trace of Density Matrix is not 1"

    return random_density_matrix

"""
TODO: Figure out how to optimize, takes 11 minutes for num_tests = 10!!!
"""
def get_error_rates(num_tests):
    W_error = 0
    Wp_error = 0

    for test in range(num_tests):
        rho = create_random_rho()
        rho = Matrix(rho.tolist())
        entangled = PPT_test(rho)

        W1_v = trigsimp(simplify(Trace(W1*rho)))
        W2_v = trigsimp(simplify(Trace(W2*rho)))
        W3_v = trigsimp(simplify(Trace(W3*rho)))
        W4_v = trigsimp(simplify(Trace(W4*rho)))
        W5_v = trigsimp(simplify(Trace(W5*rho)))
        W6_v = trigsimp(simplify(Trace(W6*rho)))

        W1_min = optimize_W(W1_v)
        W2_min = optimize_W(W2_v)
        W3_min = optimize_W(W3_v)
        W4_min = optimize_W(W4_v)
        W5_min = optimize_W(W5_v)
        W6_min = optimize_W(W6_v)

        if entangled == True and min(W1_min, W2_min, W3_min, W4_min, W5_min, W6_min) >= 0:
            W_error += 1
        
        W1p_v = trigsimp(simplify(Trace(W1p*rho)))
        W2p_v = trigsimp(simplify(Trace(W2p*rho)))
        W3p_v = trigsimp(simplify(Trace(W3p*rho)))
        W4p_v = trigsimp(simplify(Trace(W4p*rho)))
        W5p_v = trigsimp(simplify(Trace(W5p*rho)))
        W6p_v = trigsimp(simplify(Trace(W6p*rho)))

        W1p_min = optimize_Wp(W1p_v)
        W2p_min = optimize_Wp(W2p_v)
        W3p_min = optimize_Wp(W3p_v)
        W4p_min = optimize_Wp(W4p_v)
        W5p_min = optimize_Wp(W5p_v)
        W6p_min = optimize_Wp(W6p_v)

        if entangled == True and min(W1p_min, W2p_min, W3p_min, W4p_min, W5p_min, W6p_min) >= 0:
            Wp_error += 1

    W_error_rate =  W_error/num_tests
    Wp_error_rate = Wp_error/num_tests

    return W_error_rate, Wp_error_rate
        

    





