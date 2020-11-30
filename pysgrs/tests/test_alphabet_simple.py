import sys
import unittest

from pysgrs import alphabets
from pysgrs.tests.test_alphabet import TestAlphabet


class TestSimpleAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.SimpleAlphabet()


class TestGenericAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class TestGenericAlphabetInteger(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices=[-10, -6, 0, 17, 102, -9999])


class TestGenericAlphabetCharacters(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices="MNOPQR")


class TestGenericAlphabetString(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices=["AAA", "AAB", "ABA", "ABB", "BAA", "BBB"])


class TestGenericAlphabetMixed(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericMixedAlphabet("ABCDEF", indices=["AAA", -1, "ABA", 7, "BAA", 22])


class TestBinaryAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BinaryAlphabet()


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
