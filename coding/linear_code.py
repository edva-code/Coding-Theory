"""Binary linear code C[n, k] given by a generator matrix in standard form.

Standard form (note 11 of the task): G = [I_k | A], size k x n.
The matching parity-check matrix is H = [A^T | I_(n-k)], size (n-k) x n.
Over GF(2), -A^T = A^T, so no sign change is needed.
"""

import random

from coding import gf2
from coding.gf2 import Matrix, Vector


def check_parameters(n: int, k: int) -> None:
    """Raise ValueError unless 0 < k < n."""
    if not 0 < k < n:
        raise ValueError(f"need 0 < k < n, got n={n}, k={k}")


def random_generator_matrix(n: int, k: int, rng: random.Random) -> Matrix:
    """Random G = [I_k | A] where A is a k x (n-k) matrix of random bits."""
    check_parameters(n, k)
    ident = gf2.identity(k)
    return [ident[i] + [rng.randint(0, 1) for _ in range(n - k)] for i in range(k)]


class LinearCode:
    def __init__(self, generator: Matrix):
        self.G = [list(row) for row in generator]
        self.k = len(self.G)
        self.n = len(self.G[0]) if self.G else 0
        self._validate()

        # A is the part of G to the right of the identity block.
        a = [row[self.k:] for row in self.G]
        a_t = gf2.transpose(a)
        ident = gf2.identity(self.n - self.k)
        self.H = [a_t[i] + ident[i] for i in range(self.n - self.k)]

        # Sanity check: every row of G must be a codeword, i.e. G * H^T = 0.
        assert all(gf2.is_zero(row) for row in gf2.mat_mul(self.G, gf2.transpose(self.H)))

    def _validate(self) -> None:
        check_parameters(self.n, self.k)
        for i, row in enumerate(self.G):
            if len(row) != self.n:
                raise ValueError(f"row {i + 1} has length {len(row)}, expected {self.n}")
            if any(bit not in (0, 1) for bit in row):
                raise ValueError(f"row {i + 1} contains values other than 0 and 1")
        if [row[:self.k] for row in self.G] != gf2.identity(self.k):
            raise ValueError("G is not in standard form: the first k columns must be I_k")

    def encode(self, message: Vector) -> Vector:
        """Codeword c = m * G."""
        if len(message) != self.k:
            raise ValueError(f"message must have length k={self.k}, got {len(message)}")
        return gf2.vec_mat_mul(message, self.G)

    def extract_message(self, codeword: Vector) -> Vector:
        """With G in standard form the message is just the first k bits."""
        return codeword[:self.k]
