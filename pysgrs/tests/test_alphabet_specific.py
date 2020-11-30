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


class TestBaconAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BaconAlphabet()


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
