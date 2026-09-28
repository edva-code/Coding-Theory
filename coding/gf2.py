"""Arithmetic over the binary field GF(2) = {0, 1}.

Addition is XOR (1 + 1 = 0) and multiplication is AND.
A vector is a list of bits, a matrix is a list of rows (each row a vector).
"""

Vector = list[int]
Matrix = list[list[int]]


def add(u: Vector, v: Vector) -> Vector:
    """Add two vectors of the same length, bit by bit (mod 2)."""
    if len(u) != len(v):
        raise ValueError(f"length mismatch: {len(u)} vs {len(v)}")
    return [a ^ b for a, b in zip(u, v)]


def weight(v: Vector) -> int:
    """Hamming weight: the number of 1s in the vector."""
    return sum(v)


def dot(u: Vector, v: Vector) -> int:
    """Dot product of two vectors (mod 2)."""
    if len(u) != len(v):
        raise ValueError(f"length mismatch: {len(u)} vs {len(v)}")
    result = 0
    for a, b in zip(u, v):
        result ^= a & b
    return result


def transpose(m: Matrix) -> Matrix:
    """Swap rows and columns."""
    return [list(col) for col in zip(*m)]


def vec_mat_mul(v: Vector, m: Matrix) -> Vector:
    """Row vector times matrix: v * M. Used for encoding (m * G)."""
    if len(v) != len(m):
        raise ValueError(f"vector length {len(v)} does not match matrix rows {len(m)}")
    return [dot(v, col) for col in transpose(m)]


def mat_vec_mul(m: Matrix, v: Vector) -> Vector:
    """Matrix times column vector: M * v^T. Used for syndromes (H * r^T)."""
    return [dot(row, v) for row in m]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    """Matrix product A * B (mod 2)."""
    return [vec_mat_mul(row, b) for row in a]


def identity(size: int) -> Matrix:
    """Identity matrix I of the given size."""
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]


def unit_vector(n: int, i: int) -> Vector:
    """Vector e_i of length n with a single 1 at index i (0-based)."""
    v = [0] * n
    v[i] = 1
    return v


def is_zero(v: Vector) -> bool:
    """True if every bit of the vector is 0."""
    return not any(v)


def to_str(v: Vector) -> str:
    """Format a vector as a bit string, e.g. [1, 0, 1] -> '101'."""
    return "".join(str(b) for b in v)


def parse(text: str) -> Vector:
    """Parse a bit string like '1011' (spaces allowed) into a vector."""
    bits = text.replace(" ", "")
    if not bits or any(ch not in "01" for ch in bits):
        raise ValueError(f"not a binary vector: {text!r}")
    return [int(ch) for ch in bits]
