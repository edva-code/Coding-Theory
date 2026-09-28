import unittest

from coding import gf2


class TestVectors(unittest.TestCase):
    def test_add_is_xor(self):
        self.assertEqual(gf2.add([0, 0, 1, 1], [0, 1, 0, 1]), [0, 1, 1, 0])

    def test_add_to_itself_gives_zero(self):
        v = [1, 0, 1, 1]
        self.assertEqual(gf2.add(v, v), [0, 0, 0, 0])

    def test_add_length_mismatch(self):
        with self.assertRaises(ValueError):
            gf2.add([1, 0], [1])

    def test_weight(self):
        self.assertEqual(gf2.weight([1, 1, 1, 0, 0, 0]), 3)
        self.assertEqual(gf2.weight([0, 0, 0]), 0)

    def test_dot(self):
        self.assertEqual(gf2.dot([1, 1, 0], [1, 1, 1]), 0)  # 1 + 1 = 0
        self.assertEqual(gf2.dot([1, 0, 1], [1, 1, 0]), 1)

    def test_unit_vector(self):
        self.assertEqual(gf2.unit_vector(4, 2), [0, 0, 1, 0])

    def test_parse_and_to_str(self):
        self.assertEqual(gf2.parse("1 01 1"), [1, 0, 1, 1])
        self.assertEqual(gf2.to_str([1, 0, 1, 1]), "1011")
        for bad in ["", "102", "abc"]:
            with self.assertRaises(ValueError):
                gf2.parse(bad)


class TestMatrices(unittest.TestCase):
    def test_transpose(self):
        self.assertEqual(gf2.transpose([[1, 0, 1], [0, 1, 1]]), [[1, 0], [0, 1], [1, 1]])

    def test_vec_mat_mul(self):
        g = [[1, 0, 0, 1], [0, 1, 1, 1]]
        self.assertEqual(gf2.vec_mat_mul([1, 1], g), [1, 1, 1, 0])

    def test_mat_vec_mul(self):
        # [VO89] example 23: syndrome of r = 111000 is 111
        h = [[1, 0, 0, 1, 0, 1], [0, 1, 0, 1, 1, 0], [0, 0, 1, 0, 1, 1]]
        self.assertEqual(gf2.mat_vec_mul(h, [1, 1, 1, 0, 0, 0]), [1, 1, 1])

    def test_mat_mul_with_identity(self):
        a = [[1, 0, 1], [0, 1, 1]]
        self.assertEqual(gf2.mat_mul(a, gf2.identity(3)), a)


if __name__ == "__main__":
    unittest.main()
