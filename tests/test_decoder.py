import itertools
import random
import unittest

from coding import gf2
from coding.decoder import StepByStepDecoder
from coding.linear_code import LinearCode, random_generator_matrix

# [VO89] example 23 / 27, p. 73 and p. 79-80.
BOOK_H = [
    [1, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 1],
]


def all_vectors(length):
    return [list(bits) for bits in itertools.product([0, 1], repeat=length)]


class TestWeightTable(unittest.TestCase):
    def test_book_table(self):
        # Table on p. 79: syndrome -> weight of coset leader.
        decoder = StepByStepDecoder(BOOK_H)
        expected = {"000": 0, "101": 1, "011": 1, "110": 1,
                    "001": 1, "010": 1, "100": 1, "111": 2}
        for syndrome, weight in expected.items():
            self.assertEqual(decoder.weights[int(syndrome, 2)], weight, syndrome)

    def test_matches_brute_force(self):
        # Compare with the definition: minimum weight over all vectors in the coset.
        code = LinearCode(random_generator_matrix(9, 4, random.Random(3)))
        decoder = StepByStepDecoder(code.H)
        best = {}
        for v in all_vectors(code.n):
            s = decoder.syndrome(v)
            best[s] = min(best.get(s, code.n), gf2.weight(v))
        self.assertEqual(best, dict(enumerate(decoder.weights)))


class TestDecoding(unittest.TestCase):
    def test_book_example_27(self):
        decoder = StepByStepDecoder(BOOK_H)
        trace = []
        self.assertEqual(decoder.decode([1, 1, 1, 0, 0, 0], trace), [0, 1, 1, 0, 1, 0])
        # Positions tried and which flips were kept, exactly as on p. 80.
        self.assertEqual([(s.position + 1, s.new_weight, s.kept) for s in trace],
                         [(1, 1, True), (2, 1, False), (3, 1, False), (4, 1, False), (5, 0, True)])

    def test_codeword_is_unchanged(self):
        code = LinearCode(random_generator_matrix(10, 4, random.Random(5)))
        decoder = StepByStepDecoder(code.H)
        for message in all_vectors(code.k):
            c = code.encode(message)
            trace = []
            self.assertEqual(decoder.decode(c, trace), c)
            self.assertEqual(trace, [])

    def test_result_is_always_a_codeword(self):
        code = LinearCode(random_generator_matrix(8, 3, random.Random(11)))
        decoder = StepByStepDecoder(code.H)
        for r in all_vectors(code.n):
            self.assertTrue(gf2.is_zero(gf2.mat_vec_mul(code.H, decoder.decode(r))))

    def test_corrects_every_single_error_in_hamming_code(self):
        # [7,4] Hamming code: distance 3, so every single error must be fixed.
        g = [[1, 0, 0, 0, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 1],
             [0, 0, 1, 0, 0, 1, 1],
             [0, 0, 0, 1, 1, 1, 1]]
        code = LinearCode(g)
        decoder = StepByStepDecoder(code.H)
        for message in all_vectors(code.k):
            c = code.encode(message)
            for i in range(code.n):
                r = gf2.add(c, gf2.unit_vector(code.n, i))
                self.assertEqual(code.extract_message(decoder.decode(r)), message)

    def test_error_within_leader_weight_decodes_to_nearest(self):
        # The decoded word is never farther from r than the coset leader weight.
        code = LinearCode(random_generator_matrix(10, 5, random.Random(8)))
        decoder = StepByStepDecoder(code.H)
        for r in all_vectors(code.n)[::7]:
            d = gf2.weight(gf2.add(r, decoder.decode(r)))
            self.assertEqual(d, decoder.leader_weight(r))

    def test_rejects_wrong_length(self):
        with self.assertRaises(ValueError):
            StepByStepDecoder(BOOK_H).decode([1, 0, 1])


if __name__ == "__main__":
    unittest.main()
