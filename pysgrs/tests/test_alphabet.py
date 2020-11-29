import sys
import unittest

from pysgrs.alphabets import GenericAlphabet, BaseAlphabet
from pysgrs import errors
from pysgrs import settings


class TestAlphabetIndex:

    def test_types(self):
        self.assertIsInstance(self.alphabet.symbols, str)
        self.assertTrue(all([isinstance(i, (int, str)) for i in self.alphabet.indices]))

    def test_uniqueness(self):
        self.assertTrue(len(set(self.alphabet.symbols)) == len(self.alphabet.symbols))
        self.assertTrue(len(set(self.alphabet.indices)) == len(self.alphabet.indices))

    def test_mapping(self):
        self.assertEqual(len(self.alphabet.symbols), len(self.alphabet.indices))

    def test_indexer(self):
        for s, k in zip(self.alphabet.symbols, self.alphabet.indices):
            self.assertEqual(s, self.alphabet.symbol(k))
            self.assertEqual(s, self.alphabet[k])
            self.assertEqual(k, self.alphabet.index(s))
            self.assertEqual(k, self.alphabet[s])


class TestAlphabetSpecificIntegerIndex(TestAlphabetIndex, unittest.TestCase):

    alphabet = BaseAlphabet()

    def test_isnatural(self):
        self.assertTrue(self.alphabet.is_natural)


class TestAlphabetSpecificIntegerIndex(TestAlphabetIndex, unittest.TestCase):

    alphabet = GenericAlphabet("ABCDEF", indices=[-10, -6, 0, 17, 102, -9999])

    def test_isnatural(self):
        self.assertFalse(self.alphabet.is_natural)


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
