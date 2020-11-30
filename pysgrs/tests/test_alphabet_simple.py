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


class TestGenericMixedAlphabetString(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices=["AAA", "AAB", "ABA", "ABB", "BAA", "BBB"])


class TestGenericStringAlphabetString(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericStringAlphabet("ABCDEF", indices=["AAA", "AAB", "ABA", "ABB", "BAA", "BBB"])


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
