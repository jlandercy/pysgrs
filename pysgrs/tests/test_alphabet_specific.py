import sys
import unittest

from pysgrs import alphabets
from pysgrs.tests.test_alphabet import TestAlphabet


class TestPolybeAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.PolybeAlphabet()


class TestMorseAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.MorseAlphabet()

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)

    def test_is_index_size_constant(self):
        self.assertFalse(self.alphabet.is_index_size_constant)

    def test_index_size(self):
        self.assertEqual(1, self.alphabet.index_min_size)
        self.assertEqual(5, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"*", "-"}, self.alphabet.index_symbols)


class TestBaconAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BaconAlphabet()

    def test_index_size(self):
        self.assertEqual(5, self.alphabet.index_min_size)
        self.assertEqual(5, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"a", "b"}, self.alphabet.index_symbols)


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
