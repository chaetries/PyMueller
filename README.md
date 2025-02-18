# Tools for Mueller Matrices

A collection of functions to manipulate and process Mueller matrix data.

This package provides tools for two primary tasks:

1. **Physical Realizability Test**  
2. **Decomposition**

Both modules have been adapted to work with single 4×4 Mueller matrices as well as with Mueller matrix images (e.g. a dataset with shape (H, W, 16)).

---

## 1. Physical Realizability Test

The **prtest** module offers several options to test the physical realizability of 4×4 Mueller matrices. These functions accept a 4×4 matrix representing a Mueller matrix and return a boolean result indicating whether the test is passed.

### Available Test Methods:
- **`charpoly`**: Characteristic Polynomial Test
- **`choletsky`**: Cholesky Decomposition Test

Additionally, the function **`build_eigen_matrix`** computes the coherency matrix required by the tests.

Performance benchmarks and detailed implementations can be found in the original repository [here](https://github.com/pogudingleb/mueller_matrices).

---

## 2. Decomposition

The **decomposition** module provides a method for decomposing a Mueller matrix image into its optical parameters using the Lu-Chipman decomposition.

### Decomposition Parameters:
- **`MMD_D`**: Diattenuation
- **`MMD_Delta`**: Depolarization
- **`MMD_LR`**: Linear Retardance
- **`MMD_CR`**: Circular Retardance
- **`MMD_psi`**: Orientation

The function **`lu_chipman`** accepts:
- **`H_image`**: Height (number of rows) of the MM image.
- **`W_image`**: Width (number of columns) of the MM image.
- **`FinalM`**: A flattened MM image with shape `(H_image, W_image, 16)`. Internally, this is reshaped into `(H_image, W_image, 4, 4)`.

*Reference*:  
Lu, S. Y., & Chipman, R. A. (1996). Interpretation of Mueller matrices based on polar decomposition. *JOSA A, 13(5), 1106-1113*.

---

## How to Install

Install the package from PyPI:

```bash
pip install pymueller
```

```python
import pymueller
```

## Example Usage

### A. Physical Realizability Tests (Single 4×4 Matrix)

```python
import numpy as np
from pymueller.prtest import build_eigen_matrix, choletsky, charpoly

# Define a sample 4×4 Mueller matrix (for example, with a small perturbation)
M = np.array([
    [1.0, 0.1, 0.2, 0.3],
    [0.1, 1.0, 0.4, 0.5],
    [0.2, 0.4, 1.0, 0.6],
    [0.3, 0.5, 0.6, 1.0]
])

# Compute the coherency matrix (if needed)
H = build_eigen_matrix(M)

# Test physical realizability using two methods
if choletsky(M):
    print("Matrix passed the Cholesky (choletsky) test.")

if charpoly(M):
    print("Matrix passed the characteristic polynomial (charpoly) test.")
```
###  B. Decomposition on a Mueller Matrix Image

If you have an MM image (e.g., from a polarimetric imaging system) with shape (H, W, 16), you can decompose it into optical parameters. For example, here we generate a synthetic dataset where each 4×4 Mueller matrix is the identity plus a small random perturbation (to avoid divisions by zero):

```python

import numpy as np
from pymueller.decomposition import lu_chipman

# Define image dimensions
H, W = 500, 500

# Create a synthetic MM image where each pixel is an identity 4×4 plus a small random noise.
identity = np.eye(4)
noise = np.random.uniform(low=-0.1, high=0.1, size=(H, W, 4, 4))
mm_matrices = identity + noise
# Reshape to (H, W, 16) as expected by lu_chipman
FinalM = mm_matrices.reshape(H, W, 16)

# Perform Lu-Chipman decomposition
MMD_D, MMD_Delta, MMD_LR, MMD_CR, MMD_psi = lu_chipman(H, W, FinalM)

print("Diattenuation (MMD_D):", MMD_D)
print("Depolarization (MMD_Delta):", MMD_Delta)
print("Linear Retardance (MMD_LR):", MMD_LR)
print("Circular Retardance (MMD_CR):", MMD_CR)
print("Orientation (MMD_psi):", MMD_psi)

```

## Running the Tests

 Running the Tests

The repository includes tests that:
* Generate synthetic MM image datasets. 
* Loop through selected pixels to verify the physical realizability tests.
* Validate the decomposition outputs for a full MM image.
To run all tests, simply execute:
```bash
 python -m unittest discover -s tests
```