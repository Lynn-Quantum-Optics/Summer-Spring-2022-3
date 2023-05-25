import numpy as np


SIGMA_X = np.matrix([
    [0, 1],
    [1, 0]
])
SIGMA_Y = np.matrix([
    [0, -1j],
    [1j, 0]
])
SIGMA_Z = np.matrix([
    [1, 0],
    [0, -1]
])


def adjoint(matrix):
    transpose = np.transpose(matrix)
    return np.conjugate(transpose)


def partial_transpose(density_matrix):
    new_matrix = density_matrix.copy()

    for r1 in [0, 1]:
        for c1 in [0, 1]:
            for r2 in [0, 1]:
                for c2 in [0, 1]:
                    if r2 != c2:
                        new_matrix[2 * r1 + r2, 2 * c1 + c2] = density_matrix[2 * r1 + c2, 2 * c1 + r2]

    return new_matrix


def create_pure_state_vector(theta, alpha, beta, phi_1, phi_2, phi_3):
    state_vector = np.matrix([
        [np.cos(theta) * np.cos(alpha)],
        [np.exp(1j * phi_1) * np.cos(theta) * np.sin(alpha)],
        [np.exp(1j * phi_2) * np.sin(theta) * np.sin(beta)],
        [np.exp(1j * phi_3) * np.sin(theta) * np.cos(beta)],
    ])

    return state_vector


PHI_PLUS = create_pure_state_vector(np.pi / 4, 0, 0, 0, 0, 0)
PHI_MINUS = create_pure_state_vector(- np.pi / 4, 0, 0, 0, 0, 0)
PSI_PLUS = create_pure_state_vector(np.pi / 4, np.pi / 2, np.pi / 2, 0, 0, 0)
PSI_MINUS = create_pure_state_vector(- np.pi / 4, np.pi / 2, np.pi / 2, 0, 0, 0)


def create_density_matrix(state_vector):
    density_matrix = state_vector * adjoint(state_vector)

    return density_matrix


def calculate_expectation_value(operator, density_matrix):
    return round(np.trace(operator * density_matrix).real, 3)


def evolve_density_matrix(density_matrix, operator, normalize=True):
    unnormalized = operator * density_matrix * adjoint(operator)
    return unnormalized / np.trace(unnormalized) if normalize else unnormalized


# UNTESTED
def devolve_density_matrix(density_matrix, operator):
    unnormalized = adjoint(operator) * density_matrix * operator
    return unnormalized / np.trace(unnormalized)


# UNTESTED
def calculate_concurrence(density_matrix):
    sqrt_rho = get_sqrt_matrix(density_matrix)
    spin_flip = np.kron(SIGMA_Y, SIGMA_Y)
    spin_flip_rho = spin_flip * density_matrix * spin_flip
    M = get_sqrt_matrix(
        sqrt_rho * spin_flip_rho * sqrt_rho
    )
    largest_eigenvalue = max(np.linalg.eigvals(M))
    return round(max(0, 2 * largest_eigenvalue - np.trace(M)).real, 3)


# UNTESTED
def get_sqrt_matrix(density_matrix):
    # https://stackoverflow.com/questions/61262772/is-there-any-way-to-get-a-sqrt-of-a-matrix-in-numpy-not-element-wise-but-as-a
    eigenvalues, eigenvectors = np.linalg.eig(density_matrix)

    sqrt_matrix = eigenvectors * np.diag(np.sqrt(eigenvalues)) * adjoint(eigenvectors)

    return sqrt_matrix


def check_entanglement(density_matrix):
    eigenvalues = np.linalg.eigvals(partial_transpose(density_matrix))
    for eigenvalue in eigenvalues:
        if round(eigenvalue, 3) < 0:
            return True
    return False