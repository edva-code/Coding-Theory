"""Step-by-step decoding for binary linear codes [VO89, §3.7, p. 78-81].

Precomputation: a table from every syndrome to the weight of its coset leader.
Decoding (p. 79):
    (1) set i = 1
    (2) compute H r^T and the weight w of the corresponding coset leader
    (3) if w = 0, stop with r as the transmitted codeword
    (4) if H (r + e_i)^T has smaller associated weight than H r^T, set r = r + e_i
    (5) set i = i + 1 and go to (2)

Implementation note: syndromes are stored as integers (bit j of the integer is
row j of H), so H v^T is simply the XOR of the columns of H at the positions
where v has a 1. Flipping bit i of r therefore changes the syndrome by
XOR-ing column i of H - we never need to multiply the whole matrix again.
"""

from dataclasses import dataclass

from coding import gf2
from coding.gf2 import Matrix, Vector


def _column_to_int(column: Vector) -> int:
    value = 0
    for bit in column:
        value = (value << 1) | bit
    return value


def _int_to_vector(value: int, length: int) -> Vector:
    return [(value >> (length - 1 - j)) & 1 for j in range(length)]


@dataclass
class DecodeStep:
    """One iteration of the decoding loop, kept for showing to the user."""
    position: int        # 0-based index i of the bit that was tried
    old_weight: int      # coset leader weight before trying the flip
    new_syndrome: Vector
    new_weight: int      # coset leader weight if bit i were flipped
    kept: bool           # True if the flip was kept


class StepByStepDecoder:
    def __init__(self, parity_check: Matrix):
        self.H = [list(row) for row in parity_check]
        self.r = len(self.H)          # number of syndrome bits, n - k
        self.n = len(self.H[0])
        self.columns = [_column_to_int(col) for col in gf2.transpose(self.H)]
        self.weights = self._build_weight_table()

    def _build_weight_table(self) -> list[int]:
        """weights[s] = weight of the coset leader for syndrome s.

        Same idea as in the book: look at error vectors in order of increasing
        weight, and the first one that gives syndrome s is a coset leader.
        Instead of listing all error vectors of weight w, we take the
        syndromes reached with w-1 errors and add one more column of H.
        A syndrome is new at level w exactly when no error vector of weight
        < w produces it, so each syndrome gets its minimum weight.
        """
        size = 2 ** self.r
        weights = [-1] * size
        weights[0] = 0
        frontier = [0]
        w = 0
        while frontier:
            w += 1
            next_frontier = []
            for s in frontier:
                for col in self.columns:
                    t = s ^ col
                    if weights[t] == -1:
                        weights[t] = w
                        next_frontier.append(t)
            frontier = next_frontier
        if -1 in weights:
            raise ValueError("H does not have full rank: some syndromes are unreachable")
        return weights

    def syndrome(self, v: Vector) -> int:
        """H v^T as an integer: XOR of the columns of H where v has a 1."""
        s = 0
        for bit, col in zip(v, self.columns):
            if bit:
                s ^= col
        return s

    def syndrome_vector(self, v: Vector) -> Vector:
        return _int_to_vector(self.syndrome(v), self.r)

    def leader_weight(self, v: Vector) -> int:
        return self.weights[self.syndrome(v)]

    def decode(self, received: Vector, trace: list[DecodeStep] | None = None) -> Vector:
        """Return the codeword that step-by-step decoding finds for `received`.

        If `trace` is given, every tried position is appended to it.
        """
        if len(received) != self.n:
            raise ValueError(f"vector must have length n={self.n}, got {len(received)}")
        r = list(received)
        s = self.syndrome(r)                  # step (2)
        w = self.weights[s]
        # Steps (1) and (5): go through positions in order. The book does not
        # say what happens after i = n, so the loop simply ends there.
        for i in range(self.n):
            if w == 0:                        # step (3)
                break
            s_flipped = s ^ self.columns[i]   # syndrome of r + e_i
            w_flipped = self.weights[s_flipped]
            kept = w_flipped < w              # step (4)
            if trace is not None:
                trace.append(DecodeStep(i, w, _int_to_vector(s_flipped, self.r), w_flipped, kept))
            if kept:
                r[i] ^= 1
                s, w = s_flipped, w_flipped
        return r
