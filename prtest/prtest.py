#prtest/prtest.py

def build_eigen_matrix(M):
    """Calculate the elements of the hypothesized Mueller matrix H(M) from the measured Mueller matrix M.

    Args:
        M: The measured Mueller matrix.

    Returns:
        The coherency matrix H(M).
    """


    H = np.zeros((4, 4), dtype=np.complex128)

    H[0, 0] = M[0, 0] + M[0, 1] + M[1, 0] + M[1, 1]
    H[0, 1] = M[0, 2] + M[1, 2] + 1j * (M[0, 3] + M[1, 3])
    H[0, 2] = M[2, 0] + M[2, 1] - 1j * (M[3, 0] + M[3, 1])
    H[0, 3] = M[2, 2] + M[3, 3] + 1j * (M[2, 3] - M[3, 2])

    H[1, 0] = np.conj(H[0, 1])
    H[1, 1] = M[0, 0] - M[0, 1] + M[1, 0] - M[1, 1]
    H[1, 2] = M[2, 2] - M[3, 3] - 1j * (M[2, 3] + M[3, 2])
    H[1, 3] = M[2, 0] - M[2, 1] - 1j * (M[3, 0] - M[3, 1])

    H[2, 0] = np.conj(H[0, 2])
    H[2, 1] = np.conj(H[1, 2])
    H[2, 2] = M[0, 0] + M[0, 1] - M[1, 0] - M[1, 1]
    H[2, 3] = M[0, 2] - M[1, 2] + 1j * (M[0, 3] - M[1, 3])

    H[3, 0] = np.conj(H[0, 3])
    H[3, 1] = np.conj(H[1, 3])
    H[3, 2] = np.conj(H[2, 3])
    H[3, 3] = M[0, 0] - M[0, 1] - M[1, 0] + M[1, 1]



    return H

def choletsky(M):
    """
    Check if a given matrix M can be decomposed using Cholesky decomposition.

    Parameters:
    - M (numpy.ndarray): A 4x4 complex matrix.

    Returns:
    - bool: True if the matrix can be decomposed using Cholesky, False otherwise.
    """
    H = build_eigen_matrix(M)
    try:
        # Perform Cholesky decomposition
        L = np.linalg.cholesky(H)
        return True
    except np.linalg.LinAlgError:
        return False

def charpoly(M, verbose=False):
    C1 = M[0, 0]

    C2 = (3 * M[0, 0]**2 - M[0, 1]**2 - M[0, 2]**2 - M[0, 3]**2 -
          M[1, 0]**2 - M[1, 1]**2 - M[1, 2]**2 - M[1, 3]**2 -
          M[2, 0]**2 - M[2, 1]**2 - M[2, 2]**2 - M[2, 3]**2 -
          M[3, 0]**2 - M[3, 1]**2 - M[3, 2]**2 - M[3, 3]**2)

    C3 = (4 * M[0, 0]**3 +
          (-4 * M[0, 1]**2 - 4 * M[0, 2]**2 - 4 * M[0, 3]**2 -
           -4 * M[1, 0]**2 - 4 * M[1, 1]**2 - 4 * M[1, 2]**2 - 4 * M[1, 3]**2 -
           -4 * M[2, 0]**2 - 4 * M[2, 1]**2 - 4 * M[2, 2]**2 - 4 * M[2, 3]**2 -
           -4 * M[3, 0]**2 - 4 * M[3, 1]**2 - 4 * M[3, 2]**2 - 4 * M[3, 3]**2) * M[0, 0] +
          (8 * M[1, 0] * M[1, 1] + 8 * M[2, 0] * M[2, 1] + 8 * M[3, 0] * M[3, 1]) * M[0, 1] +
          (8 * M[1, 0] * M[1, 2] + 8 * M[2, 0] * M[2, 2] + 8 * M[3, 0] * M[3, 2]) * M[0, 2] +
          (8 * M[1, 0] * M[1, 3] + 8 * M[2, 0] * M[2, 3] + 8 * M[3, 0] * M[3, 3]) * M[0, 3] +
          (8 * M[2, 2] * M[3, 3] - 8 * M[2, 3] * M[3, 2]) * M[1, 1] +
          (-8 * M[2, 1] * M[3, 3] + 8 * M[2, 3] * M[3, 1]) * M[1, 2] +
          8 * M[1, 3] * (M[2, 1] * M[3, 2] - M[2, 2] * M[3, 1]))

    C4 = (M[0, 0]**4 + M[0, 1]**4 + M[0, 2]**4 + M[1, 0]**4 +
          M[1, 1]**4 + M[1, 2]**4 + M[2, 0]**4 + M[2, 1]**4 +
          M[2, 2]**4 + M[0, 3]**4 + M[1, 3]**4 + M[2, 3]**4 +
          8 * M[2, 2] * M[2, 3] * M[3, 2] * M[3, 3] -
          8 * M[3, 0] * (M[2, 1] * M[3, 1] + M[2, 2] * M[3, 2] + M[2, 3] * M[3, 3]) * M[2, 0] +
          8 * M[3, 1] * (M[2, 2] * M[3, 2] + M[2, 3] * M[3, 3]) * M[2, 1] +
          8 * M[1, 3] * (M[2, 2] * M[2, 3] + M[3, 2] * M[3, 3]) * M[1, 2] +
          (M[3, 0]**2 - M[3, 1]**2 - M[3, 2]**2 - M[3, 3]**2)**2 +
          (2 * M[3, 0]**2 - 2 * M[3, 1]**2 - 2 * M[3, 2]**2 + 2 * M[3, 3]**2) * M[2, 3]**2 +
          (2 * M[2, 3]**2 + 2 * M[3, 0]**2 - 2 * M[3, 1]**2 + 2 * M[3, 2]**2 - 2 * M[3, 3]**2) * M[2, 2]**2 +
          (2 * M[2, 2]**2 + 2 * M[2, 3]**2 + 2 * M[3, 0]**2 + 2 * M[3, 1]**2 - 2 * M[3, 2]**2 - 2 * M[3, 3]**2) * M[2, 1]**2 +
          (-2 * M[2, 1]**2 - 2 * M[2, 2]**2 - 2 * M[2, 3]**2 + 2 * M[3, 0]**2 + 2 * M[3, 1]**2 + 2 * M[3, 2]**2 + 2 * M[3, 3]**2) * M[2, 0]**2 +
          (2 * M[2, 0]**2 - 2 * M[2, 1]**2 - 2 * M[2, 2]**2 + 2 * M[2, 3]**2 + 2 * M[3, 0]**2 - 2 * M[3, 1]**2 - 2 * M[3, 2]**2 + 2 * M[3, 3]**2) * M[1, 3]**2 +
          (2 * M[1, 3]**2 + 2 * M[2, 0]**2 - 2 * M[2, 1]**2 + 2 * M[2, 2]**2 - 2 * M[2, 3]**2 + 2 * M[3, 0]**2 - 2 * M[3, 1]**2 + 2 * M[3, 2]**2 - 2 * M[3, 3]**2) * M[1, 2]**2 +
          ((8 * M[2, 1] * M[2, 2] + 8 * M[3, 1] * M[3, 2]) * M[1, 2] +
          8 * M[1, 3] * (M[2, 1] * M[2, 3] + M[3, 1] * M[3, 3])) * M[1, 1] +
          (2 * M[1, 2]**2 + 2 * M[1, 3]**2 + 2 * M[2, 0]**2 + 2 * M[2, 1]**2 - 2 * M[2, 2]**2 - 2 * M[2, 3]**2 + 2 * M[3, 0]**2 + 2 * M[3, 1]**2 - 2 * M[3, 2]**2 - 2 * M[3, 3]**2) * M[1, 1]**2 +
          ((-8 * M[2, 0] * M[2, 1] - 8 * M[3, 0] * M[3, 1]) * M[1, 1] + (-8 * M[2, 0] * M[2, 2] - 8 * M[3, 0] * M[3, 2]) * M[1, 2] -
          8 * M[1, 3] * (M[2, 0] * M[2, 3] + M[3, 0] * M[3, 3])) * M[1, 0] +
          (-2 * M[1, 1]**2 - 2 * M[1, 2]**2 - 2 * M[1, 3]**2 + 2 * M[2, 0]**2 + 2 * M[2, 1]**2 + 2 * M[2, 2]**2 + 2 * M[2, 3]**2 + 2 * M[3, 0]**2 + 2 * M[3, 1]**2 + 2 * M[3, 2]**2 + 2 * M[3, 3]**2) * M[1, 0]**2 +
          ((-8 * M[2, 1] * M[3, 2] + 8 * M[2, 2] * M[3, 1]) * M[1, 0] +
          (8 * M[2, 0] * M[3, 2] - 8 * M[2, 2] * M[3, 0]) * M[1, 1] +
          8 * M[1, 2] * (-M[2, 0] * M[3, 1] + M[2, 1] * M[3, 0])) * M[0, 3] +
          (-2 * M[1, 0]**2 + 2 * M[1, 1]**2 + 2 * M[1, 2]**2 - 2 * M[1, 3]**2 - 2 * M[2, 0]**2 + 2 * M[2, 1]**2 + 2 * M[2, 2]**2 - 2 * M[2, 3]**2 - 2 * M[3, 0]**2 + 2 * M[3, 1]**2 + 2 * M[3, 2]**2 - 2 * M[3, 3]**2) * M[0, 3]**2 +
          ((-8 * M[1, 2] * M[1, 3] - 8 * M[2, 2] * M[2, 3] - 8 * M[3, 2] * M[3, 3]) * M[0, 3] +
          (8 * M[2, 1] * M[3, 3] - 8 * M[2, 3] * M[3, 1]) * M[1, 0] +
          (-8 * M[2, 0] * M[3, 3] + 8 * M[2, 3] * M[3, 0]) * M[1, 1] -
          8 * M[1, 3] * (-M[2, 0] * M[3, 1] + M[2, 1] * M[3, 0])) * M[0, 2] +
          (2 * M[0, 3]**2 - 2 * M[1, 0]**2 + 2 * M[1, 1]**2 - 2 * M[1, 2]**2 + 2 * M[1, 3]**2 - 2 * M[2, 0]**2 + 2 * M[2, 1]**2 - 2 * M[2, 2]**2 + 2 * M[2, 3]**2 - 2 * M[3, 0]**2 + 2 * M[3, 1]**2 - 2 * M[3, 2]**2 + 2 * M[3, 3]**2) * M[0, 2]**2 +
          ((-8 * M[1, 1] * M[1, 2] - 8 * M[2, 1] * M[2, 2] - 8 * M[3, 1] * M[3, 2]) * M[0, 2] +
          (-8 * M[1, 1] * M[1, 3] - 8 * M[2, 1] * M[2, 3] - 8 * M[3, 1] * M[3, 3]) * M[0, 3] +
          (-8 * M[2, 2] * M[3, 3] + 8 * M[2, 3] * M[3, 2]) * M[1, 0] +
          (8 * M[2, 0] * M[3, 3] - 8 * M[2, 3] * M[3, 0]) * M[1, 2] +
          8 * M[1, 3] * (-M[2, 0] * M[3, 2] + M[2, 2] * M[3, 0])) * M[0, 1] +
          (2 * M[0, 2]**2 + 2 * M[0, 3]**2 - 2 * M[1, 0]**2 - 2 * M[1, 1]**2 + 2 * M[1, 2]**2 + 2 * M[1, 3]**2 - 2 * M[2, 0]**2 - 2 * M[2, 1]**2 + 2 * M[2, 2]**2 + 2 * M[2, 3]**2 - 2 * M[3, 0]**2 - 2 * M[3, 1]**2 + 2 * M[3, 2]**2 + 2 * M[3, 3]**2) * M[0, 1]**2 +
          ((8 * M[1, 0] * M[1, 1] + 8 * M[2, 0] * M[2, 1] + 8 * M[3, 0] * M[3, 1]) * M[0, 1] +
          (8 * M[1, 0] * M[1, 2] + 8 * M[2, 0] * M[2, 2] + 8 * M[3, 0] * M[3, 2]) * M[0, 2] +
          (8 * M[1, 0] * M[1, 3] + 8 * M[2, 0] * M[2, 3] + 8 * M[3, 0] * M[3, 3]) * M[0, 3] +
          (8 * M[2, 2] * M[3, 3] - 8 * M[2, 3] * M[3, 2]) * M[1, 1] +
          (-8 * M[2, 1] * M[3, 3] + 8 * M[2, 3] * M[3, 1]) * M[1, 2] +
          8 * M[1, 3] * (M[2, 1] * M[3, 2] - M[2, 2] * M[3, 1])) * M[0, 0] +
          (-2 * M[0, 1]**2 - 2 * M[0, 2]**2 - 2 * M[0, 3]**2 - 2 * M[1, 0]**2 -
          2 * M[1, 1]**2 - 2 * M[1, 2]**2 - 2 * M[1, 3]**2 - 2 * M[2, 0]**2 -
          2 * M[2, 1]**2 - 2 * M[2, 2]**2 - 2 * M[2, 3]**2 - 2 * M[3, 0]**2 -
          2 * M[3, 1]**2 - 2 * M[3, 2]**2 - 2 * M[3, 3]**2) * M[0, 0]**2)
    if verbose:
        print(f"C1: {C1}")
        print(f"C2: {C2}")
        print(f"C3: {C3}")
        print(f"C4: {C4}")

    return ((C1 >= 0) and (C2 >= 0) and (C3 >= 0)and (C4 >= 0))