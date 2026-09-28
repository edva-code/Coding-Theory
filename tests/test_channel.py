import random
import unittest

from coding.channel import BinarySymmetricChannel


class TestChannel(unittest.TestCase):
    def test_pe_zero_changes_nothing(self):
        channel = BinarySymmetricChannel(0.0, random.Random(1))
        self.assertEqual(channel.transmit([1, 0, 1, 1]), ([1, 0, 1, 1], []))

    def test_pe_one_flips_everything(self):
        channel = BinarySymmetricChannel(1.0, random.Random(1))
        self.assertEqual(channel.transmit([1, 0, 1]), ([0, 1, 0], [0, 1, 2]))

    def test_reported_errors_match_the_difference(self):
        channel = BinarySymmetricChannel(0.3, random.Random(7))
        sent = [0] * 100
        received, errors = channel.transmit(sent)
        self.assertEqual(errors, [i for i, b in enumerate(received) if b])

    def test_error_rate_is_close_to_pe(self):
        channel = BinarySymmetricChannel(0.1, random.Random(42))
        _, errors = channel.transmit([0] * 100_000)
        self.assertAlmostEqual(len(errors) / 100_000, 0.1, delta=0.01)

    def test_rejects_bad_probability(self):
        for pe in [-0.1, 1.5]:
            with self.assertRaises(ValueError):
                BinarySymmetricChannel(pe, random.Random())


if __name__ == "__main__":
    unittest.main()
