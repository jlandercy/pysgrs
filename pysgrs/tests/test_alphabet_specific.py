import sys
import unittest

from pysgrs import alphabets
from pysgrs.tests.test_alphabet import TestAlphabet
from pysgrs import errors


class TestPolybeAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.PolybeAlphabet()


class TestStringAlphabet(TestAlphabet):

    def test_parser_with_size_hint(self):
        for message in self.messages:
            for parsed in self.alphabet.parse(message[0], max_length=len(message[1])):
                if message[1] == parsed:
                    break
            else:
                raise errors.IllegalAlphabetOperation("Cannot decode message '{}' from '{}'".format(
                    message[1], message[0]
                ))

    def test_parser_without_size_hint(self):
        for message in self.messages:
            for parsed in self.alphabet.parse(message[0]):
                if message[1] == parsed:
                    break
            else:
                raise errors.IllegalAlphabetOperation("Cannot decode message '{}' from '{}'".format(
                    message[1], message[0]
                ))


class TestMorseAlphabet(TestStringAlphabet, unittest.TestCase):

    alphabet = alphabets.MorseAlphabet()
    messages = [
        ('******-***-**---', "HELLO"),
        ('*--*-*--*', "ACME"),
        ('*---**--*', "JEAN"),
    ]

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)

    def test_is_index_size_constant(self):
        self.assertFalse(self.alphabet.is_index_size_constant)

    def test_index_size(self):
        self.assertEqual(1, self.alphabet.index_min_size)
        self.assertEqual(5, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"*", "-"}, self.alphabet.index_symbols)


class TestBaconAlphabet(TestStringAlphabet, unittest.TestCase):

    alphabet = alphabets.BaconAlphabet()
    messages = [
        ('aabbbaabaaababaababaabbab', "HELLO"),
        ('aaaaaaaabaababbaabaa', "ACME"),
        ('abaaaaabaaaaaaaabbaa', "IEAN"),
    ]

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
