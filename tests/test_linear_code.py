import random
import unittest

from coding import gf2
from coding.linear_code import LinearCode, random_generator_matrix

G_63 = [
    [1, 0, 0, 0, 1, 1],
    [0, 1, 0, 1, 0, 1],
    [0, 0, 1, 1, 1, 0],
]


class TestLinearCode(unittest.TestCase):
    def test_parity_check_matrix(self):
        code = LinearCode(G_63)
        self.assertEqual(code.H, [
            [0, 1, 1, 1, 0, 0],
            [1, 0, 1, 0, 1, 0],
            [1, 1, 0, 0, 0, 1],
        ])

    def test_encode(self):
        code = LinearCode(G_63)
        self.assertEqual(code.encode([1, 0, 1]), [1, 0, 1, 1, 0, 1])

    def test_codewords_have_zero_syndrome_and_keep_message(self):
        code = LinearCode(G_63)
        for m in range(2 ** code.k):
            message = [(m >> (code.k - 1 - i)) & 1 for i in range(code.k)]
            c = code.encode(message)
            self.assertTrue(gf2.is_zero(gf2.mat_vec_mul(code.H, c)))
            self.assertEqual(code.extract_message(c), message)

    def test_rejects_bad_matrices(self):
        bad = [
            [[1, 0, 1], [1, 1, 0]],           # not standard form
            [[1, 0, 1], [0, 1]],              # ragged rows
            [[1, 0, 2], [0, 1, 1]],           # not binary
            [[1, 0], [0, 1]],                 # k == n
        ]
        for g in bad:
            with self.assertRaises(ValueError):
                LinearCode(g)

    def test_encode_rejects_wrong_length(self):
        with self.assertRaises(ValueError):
            LinearCode(G_63).encode([1, 0])

    def test_random_generator_is_standard_form(self):
        rng = random.Random(1)
        for n, k in [(7, 4), (10, 3), (15, 11)]:
            code = LinearCode(random_generator_matrix(n, k, rng))
            self.assertEqual((code.n, code.k), (n, k))

    def test_random_generator_rejects_bad_parameters(self):
        with self.assertRaises(ValueError):
            random_generator_matrix(4, 4, random.Random())


if __name__ == "__main__":
    unittest.main()
