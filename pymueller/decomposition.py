# decomposition/decomposition.py
import numpy as np
import cv2
import time
def lu_chipman(H_image, W_image, FinalM, se_size=1):
    # Reshape FinalM to the correct image format
    FinalM = FinalM.reshape(H_image, W_image, 4, 4)

    # Initialize arrays for MMD parameters
    MMD_D = np.zeros((H_image, W_image))
    MMD_Delta = np.zeros((H_image, W_image))
    MMD_LR = np.zeros((H_image, W_image))
    MMD_R = np.zeros((H_image, W_image))
    MMD_CR = np.zeros((H_image, W_image))
    MMD_psi = np.zeros((H_image, W_image))

    start_time = time.time()
    for C_x in range(H_image):
        for C_y in range(W_image):
            M = FinalM[C_x, C_y, :, :]

            if M[0, 0] != 0:
                M /= M[0, 0]

                # Check and replace NaNs and Infs with zeros
                M = np.nan_to_num(M)

                D = np.sqrt(M[0, 1] ** 2 + M[0, 2] ** 2 + M[0, 3] ** 2)
                if D > 1:
                    M[0, 1] /= D
                    M[0, 2] /= D
                    M[0, 3] /= D
                    D = 1

                D_vector = np.array([M[0, 1], M[0, 2], M[0, 3]])
                m_D = np.sqrt(1 - D ** 2) * np.eye(3) + (1 - np.sqrt(1 - D ** 2)) * np.outer(D_vector, D_vector)
                M_D = np.vstack([np.hstack(([1], D_vector)), np.hstack((D_vector[:, None], m_D))])

                if np.linalg.det(M_D) != 0:
                    M_plus = np.dot(M, np.linalg.inv(M_D))
                    m_plus = M_plus[1:4, 1:4]
                    temp_m_plus = np.dot(m_plus, m_plus.T)
                    lamda = np.linalg.eigvals(temp_m_plus)
                    if np.linalg.det(m_plus) != 0:
                        m_delta = np.linalg.inv(temp_m_plus + (
                                    np.sqrt(lamda[0] * lamda[1]) + np.sqrt(lamda[1] * lamda[2]) + np.sqrt(
                                lamda[0] * lamda[2])) * np.eye(3)) @ \
                                  ((np.sqrt(lamda[0]) + np.sqrt(lamda[1]) + np.sqrt(lamda[2])) * temp_m_plus + np.sqrt(
                                      lamda[0] * lamda[1] * lamda[2]) * np.eye(3)) * np.sign(np.linalg.det(m_plus))
                        delta = 1 - abs(np.trace(m_delta)) / 3
                        m_R = np.linalg.inv(m_delta) @ m_plus
                        R = np.arccos((1 + np.trace(m_R)) / 2 - 1)
                        LR = np.arccos(np.sqrt((m_R[0, 0] + m_R[1, 1]) ** 2 + (m_R[1, 0] - m_R[0, 1]) ** 2) - 1)
                        CR = 0.5 * np.arctan((m_R[1, 0] - m_R[0, 1]) / (m_R[0, 0] + m_R[1, 1]))
                        LR = np.real(LR)
                        CR = np.real(CR)
                        m_CR = np.array([[np.cos(2 * CR), np.sin(2 * CR), 0],
                                         [-np.sin(2 * CR), np.cos(2 * CR), 0],
                                         [0, 0, 1]])
                        m_LR = m_R @ np.linalg.inv(m_CR)
                        r1 = 1 / (2 * np.sin(LR)) * (m_LR[1, 2] - m_LR[2, 1])
                        r2 = 1 / (2 * np.sin(LR)) * (m_LR[2, 0] - m_LR[0, 2])
                        r1 = np.real(r1)
                        r2 = np.real(r2)
                        psi = 0.5 * np.degrees(np.arctan2(r2, r1))
                    else:
                        V, DD = np.linalg.eig(temp_m_plus)
                        V = np.atleast_2d(V)  # Ensure V is always 2-dimensional

                        # Debugging prints to check dimensions
                        # print("Shape of initial V:", V.shape)

                        # Reshape V to (3, 3) if necessary
                        if V.shape != (3, 3):  # Handle case where V might be transposed or incorrectly shaped
                            V = np.eye(3)

                        DD_diag = np.diag(np.sqrt(lamda))  # Convert eigenvalues to diagonal matrix
                        inv_sqrt_DD = np.linalg.pinv(
                            DD_diag)  # Compute the pseudo-inverse of the square root of the diagonal matrix

                        # Debugging prints to check dimensions
                        # print("Shape of reshaped V:", V.shape)
                        # print("Shape of inv_sqrt_DD:", inv_sqrt_DD.shape)
                        # print("Shape of m_plus:", m_plus.shape)

                        U_T = inv_sqrt_DD @ np.linalg.pinv(V) @ m_plus  # Use pinv for V as well
                        U = U_T.T
                        m_delta = np.sign(np.linalg.det(m_plus)) * (
                                np.sqrt(lamda[0]) * np.outer(V[:, 0], V[:, 0]) +
                                np.sqrt(lamda[1]) * np.outer(V[:, 1], V[:, 1]) +
                                np.sqrt(lamda[2]) * np.outer(V[:, 2], V[:, 2])
                        )
                        m_R = np.sign(np.linalg.det(m_plus)) * (
                                np.outer(V[:, 0], U[:, 0]) +
                                np.outer(V[:, 1], U[:, 1]) +
                                np.outer(V[:, 2], U[:, 2])
                        )
                        delta = 1 - abs(np.trace(m_delta)) / 3
                        R = np.real(np.arccos((1 + np.trace(m_R)) / 2 - 1))
                        LR = np.real(
                            np.arccos(np.sqrt((m_R[0, 0] + m_R[1, 1]) ** 2 + (m_R[1, 0] - m_R[0, 1]) ** 2) - 1))
                        CR = 0.5 * np.arctan((m_R[1, 0] - m_R[0, 1]) / (m_R[0, 0] + m_R[1, 1]))
                        m_CR = np.array([
                            [np.cos(2 * CR), np.sin(2 * CR), 0],
                            [-np.sin(2 * CR), np.cos(2 * CR), 0],
                            [0, 0, 1]
                        ])
                        m_CR += 1e-10 * np.eye(3)  # Add a small perturbation to ensure SVD convergence
                        # Use try-except block to handle SVD non-convergence
                        try:
                            m_LR = m_R @ np.linalg.pinv(m_CR)
                        except np.linalg.LinAlgError:
                            # In case of SVD non-convergence, use identity matrix as fallback
                            m_LR = m_R @ np.eye(3)

                        r1 = 1 / (2 * np.sin(LR)) * (m_LR[1, 2] - m_LR[2, 1])
                        r2 = 1 / (2 * np.sin(LR)) * (m_LR[2, 0] - m_LR[0, 2])
                        r1 = np.real(r1)
                        r2 = np.real(r2)
                        psi = 0.5 * np.degrees(np.arctan2(r2, r1))
                else:
                    P_vector = np.array([M[1, 0], M[2, 0], M[3, 0]]) / M[0, 0]
                    P_module = np.linalg.norm(P_vector)
                    P_unit = P_vector / P_module
                    delta = 1 - P_module
                    R_vector = np.cross(P_unit, D_vector) / np.linalg.norm(np.cross(P_unit, D_vector)) * np.arccos(
                        np.dot(P_unit, D_vector))
                    R = np.linalg.norm(R_vector)
                    D = 0
                    delta = 0
                    LR = 0
                    psi = 0
                    CR = 0

                MMD_D[C_x, C_y] = D  # Dichroism
                MMD_Delta[C_x, C_y] = delta  # Depolarization
                MMD_LR[C_x, C_y] = LR
                MMD_CR[C_x, C_y] = CR
                MMD_psi[C_x, C_y] = np.radians(psi)  # Fast axis

    # Apply blurring (filtering)
    MMD_D = cv2.blur(MMD_D, (se_size, se_size))
    MMD_LR = cv2.blur(MMD_LR, (se_size, se_size))
    MMD_psi = cv2.blur(MMD_psi, (se_size, se_size))
    MMD_Delta = cv2.blur(np.abs(MMD_Delta), (se_size, se_size))
    MMD_CR = cv2.blur(MMD_CR, (se_size, se_size))

    print('MMD parameter calculation completed!')
    print(f'Elapsed time: {time.time() - start_time} seconds')

    return MMD_D, MMD_Delta, MMD_LR, MMD_CR, MMD_psi
