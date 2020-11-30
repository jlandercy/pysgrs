import sys
import unittest

from pysgrs import alphabets
from pysgrs import errors
from pysgrs.tests.test_alphabet import TestAlphabet


class TestSimpleAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.SimpleAlphabet()


class TestGenericMixedAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class TestGenericIntegerAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericIntegerAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class TestGenericMixedAlphabetInteger(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices=[-10, -6, 0, 17, 102, -9999])

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)


class TestGenericIntegerAlphabetInteger(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericIntegerAlphabet("ABCDEF", indices=[-10, -6, 0, 17, 102, -9999])

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)


class TestGenericMixedAlphabetCharacters(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices="MNOPQR")


class TestGenericStringAlphabetCharacters(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericStringAlphabet("ABCDEF", indices="MNOPQR")

    def test_index_size(self):
        self.assertEqual(1, self.alphabet.index_min_size)
        self.assertEqual(1, self.alphabet.index_max_size)


class TestGenericMixedAlphabetString(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices=["AAA", "AAB", "ABA", "ABB", "BAA", "BBB"])


class TestGenericStringAlphabetString(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericStringAlphabet("ABCDEF", indices=["AAA", "AAB", "ABA", "ABB", "BAA", "BBB"])

    def test_index_size(self):
        self.assertEqual(3, self.alphabet.index_min_size)
        self.assertEqual(3, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"A", "B"}, self.alphabet.index_symbols)


class TestGenericStringAlphabetStringNotMonotonic(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericStringAlphabet("ABCDEF", indices=["BBB", "AAA", "AAB", "ABA", "ABB", "BAA"])

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)

    def test_index_size(self):
        self.assertEqual(3, self.alphabet.index_min_size)
        self.assertEqual(3, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"A", "B"}, self.alphabet.index_symbols)


class TestGenericStringAlphabetStringVariableSize(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericStringAlphabet("ABCDEF", indices=["AAA", "AABB", "ABAB", "ABBB", "BAAB", "BBBB"])

    def test_is_index_size_constant(self):
        self.assertFalse(self.alphabet.is_index_size_constant)

    def test_index_size(self):
        self.assertEqual(3, self.alphabet.index_min_size)
        self.assertEqual(4, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"A", "B"}, self.alphabet.index_symbols)


class TestGenericStringAlphabetStringNotMonotonicVariableSize(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericStringAlphabet("ABCDEF", indices=["BBBB", "AAA", "AABB", "ABAB", "ABBB", "BAAB"])

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)

    def test_is_index_size_constant(self):
        self.assertFalse(self.alphabet.is_index_size_constant)

    def test_index_symbols(self):
        self.assertEqual({"A", "B"}, self.alphabet.index_symbols)


class TestGenericAlphabetMixed(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices=["AAA", -1, "ABA", 7, "BAA", 22])

    def test_is_monotonic(self):
        with self.assertRaises(errors.IllegalAlphabetOperation):
            self.alphabet.is_monotonic


class TestBinaryAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BinaryAlphabet()


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
