import unittest
import numpy as np
from pymueller.decomposition import lu_chipman


class TestDecomposition(unittest.TestCase):
    def test_lu_chipman_with_nonzero_mm_image(self):
        H, W = 500, 500
        # Create a synthetic MM image where each pixel is an identity 4x4 plus a small random noise.
        identity = np.eye(4)
        # Generate noise in the range [-0.1, 0.1] for each element.
        noise = np.random.uniform(low=-0.1, high=0.1, size=(H, W, 4, 4))
        # Combine identity and noise.
        mm_matrices = identity + noise
        # Reshape to (H, W, 16)
        FinalM = mm_matrices.reshape(H, W, 16)

        # Call the decomposition function
        MMD_D, MMD_Delta, MMD_LR, MMD_CR, MMD_psi = lu_chipman(H, W, FinalM)

        # Verify each output array has shape (H, W)
        for arr in (MMD_D, MMD_Delta, MMD_LR, MMD_CR, MMD_psi):
            self.assertIsInstance(arr, np.ndarray, "Each output should be a numpy array.")
            self.assertEqual(arr.shape, (H, W),
                             f"Expected shape ({H}, {W}), got {arr.shape}.")


if __name__ == '__main__':
    unittest.main()
