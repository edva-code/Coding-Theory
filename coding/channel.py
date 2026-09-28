"""Binary symmetric channel: every bit is flipped independently with probability pe."""

import random

from coding.gf2 import Vector


class BinarySymmetricChannel:
    def __init__(self, pe: float, rng: random.Random):
        if not 0 <= pe <= 1:
            raise ValueError(f"error probability must be in [0, 1], got {pe}")
        self.pe = pe
        # The generator is created once by the caller and reused for every
        # transmission, otherwise errors would repeat in identical patterns.
        self.rng = rng

    def transmit(self, v: Vector) -> tuple[Vector, list[int]]:
        """Send v through the channel.

        Returns the received vector and the 0-based positions that were flipped.
        """
        received = list(v)
        errors = []
        for i in range(len(received)):
            if self.rng.random() < self.pe:
                received[i] ^= 1
                errors.append(i)
        return received, errors
