import unittest
import numpy as np
from pymueller.prtest import choletsky, charpoly


class TestPRTest(unittest.TestCase):
    def setUp(self):
        # Define image dimensions
        self.H, self.W = 500, 500
        # For prtest, we can use a random dataset, but be aware that
        # the values might lead to different boolean outcomes.
        # Alternatively, you could also use a constant dataset.
        self.dataset = np.random.random((self.H, self.W, 16))

    def test_prtest_loop(self):
        # Choose a subset of random pixel indices to test (e.g., 10 pixels)
        num_tests = 10
        total_pixels = self.H * self.W
        indices = np.random.choice(total_pixels, size=num_tests, replace=False)

        for idx in indices:
            row = idx // self.W
            col = idx % self.W
            # Reshape the 16 values for this pixel into a 4x4 Mueller matrix
            matrix = self.dataset[row, col].reshape((4, 4))

            # Call the prtest functions
            result_choletsky = choletsky(matrix)
            result_charpoly = charpoly(matrix)

            # Verify that both functions return a boolean value.
            # Accept both Python bool and np.bool_.
            self.assertIsInstance(result_choletsky, (bool, np.bool_),
                                  f"choletsky output should be a boolean for pixel ({row}, {col}).")
            self.assertIsInstance(result_charpoly, (bool, np.bool_),
                                  f"charpoly output should be a boolean for pixel ({row}, {col}).")


if __name__ == '__main__':
    unittest.main()
