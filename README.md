# Tools for Mueller Matrices

A collection of functions to manipulate and process Mueller matrix data.

## 1. Physical Realizability Test
This package provides functions to test the physical realizability of 4×4 Mueller matrices. The original code, written in C++ and Julia, can be found [here](https://github.com/pogudingleb/mueller_matrices).

The `prtest` functions offer several options for physical realizability tests. These functions accept a `[4,4]` matrix representing a Mueller matrix. If the test is passed, the function returns `True`.

### Available Test Methods:
1. **`charpoly`**: Characteristic Polynomial Test
2. **`choletsky`**: Cholesky Decomposition Test

Performance benchmarks and detailed implementations can be found in the original repository.

## 2. Decomposition
This package also allows decomposition of a Mueller matrix into optical parameters, including:

- **`MMD_D`**: Diattenuation
- **`MMD_Delta`**: Depolarization
- **`MMD_LR`**: Linear Retardance
- **`MMD_CR`**: Circular Retardance
- **`MMD_psi`**: Orientation

Currently, the only available decomposition method is the **Lu-Chipman decomposition**.

## How to Run
First, install and import the necessary modules:

`pip install pymueller`

```python
import pymueller
import muellerphys
### Example Usage
```python
import numpy as np
import pymueller

M = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# Using the physical realizability test functions
H = pymueller.build_eigen_matrix(M)

if pymueller.choletsky(M):
    print("Matrix passed the Cholesky test.")

if pymueller.charpoly(M):
    print("Matrix is physically realizable.")

# Using the decomposition functions
MMD_D, MMD_Delta, MMD_LR, MMD_CR, MMD_psi = pymueller.lu_chipman(M)
print("Diattenuation:", MMD_D)
print("Depolarissation:", MMD_Delta)
print("Linear Retardance:", MMD_LR)
print("Circular Retardance:", MMD_CR)
print("Orientation:", MMD_psi)

```
