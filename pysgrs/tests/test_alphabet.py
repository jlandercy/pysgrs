import sys
import unittest

from pysgrs import alphabets
from pysgrs import errors
from pysgrs import settings


class TestAlphabet:

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
            if s == k:
                with self.assertRaises(errors.AmbiguousAlphabetIndex):
                    self.alphabet[s]
                with self.assertRaises(errors.AmbiguousAlphabetIndex):
                    self.alphabet[k]
            else:
                self.assertEqual(s, self.alphabet.symbol(k))
                self.assertEqual(s, self.alphabet[k])
                self.assertEqual(k, self.alphabet.index(s))
                self.assertEqual(k, self.alphabet[s])

    def test_illegal_indexer(self):
        with self.assertRaises(errors.IllegalAlphabetIndex):
            self.alphabet["Hello World"]
        with self.assertRaises(errors.IllegalAlphabetIndex):
            self.alphabet[-999999999990]

    def test_reversible_encoder(self):
        self.assertEqual(self.alphabet.symbols, self.alphabet.decode(self.alphabet.indices))
        self.assertEqual(self.alphabet.indices, tuple(self.alphabet.encode(self.alphabet.symbols)))
        self.assertEqual(self.alphabet.symbols, self.alphabet.decode(
            self.alphabet.encode(self.alphabet.symbols)))

    def test_isnatural(self):
        self.assertEqual(tuple(range(self.alphabet.size)) == self.alphabet.indices, self.alphabet.is_natural)


class TestBaseAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BaseAlphabet()


class TestGenericAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class TestGenericAlphabetInteger(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericAlphabet("ABCDEF", indices=[-10, -6, 0, 17, 102, -9999])


class TestGenericAlphabetCharacters(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericAlphabet("ABCDEF", indices="MNOPQR")


class TestGenericAlphabetString(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericAlphabet("ABCDEF", indices=["AAA", "AAB", "ABA", "ABB", "BAA", "BBB"])


class TestGenericAlphabetMixed(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.GenericAlphabet("ABCDEF", indices=["AAA", -1, "ABA", 7, "BAA", 22])


class TestBinaryAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BinaryAlphabet()


class TestPolybeAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.PolybeAlphabet()


class TestMorseAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.MorseAlphabet()


class TestBaconAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BaconAlphabet()


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
