import unittest

from pysgrs import alphabets
from pysgrs import errors
from pysgrs.tests.test_alphabet import TestAlphabet


class TestBasicAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BasicAlphabet()


class TestNaturalAsciiAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.AsciiAlphabet(natural=True)


class TestAsciiAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.AsciiAlphabet()


class TestMixedAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.MixedAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class TestIntegerAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.IntegerAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class TestMixedAlphabetInteger(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.MixedAlphabet("ABCDEF", indices=[-10, -6, 0, 17, 102, -9999])

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)


class TestIntegerAlphabetInteger(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.IntegerAlphabet("ABCDEF", indices=[-10, -6, 0, 17, 102, -9999])

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)


class TestMixedAlphabetCharacters(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.MixedAlphabet("ABCDEF", indices="MNOPQR")


class TestStringAlphabetCharacters(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.StringAlphabet("ABCDEF", indices="MNOPQR")

    def test_index_size(self):
        self.assertEqual(1, self.alphabet.index_min_size)
        self.assertEqual(1, self.alphabet.index_max_size)


class TestMixedAlphabetString(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.MixedAlphabet("ABCDEF", indices=["AAA", "AAB", "ABA", "ABB", "BAA", "BBB"])


class TestStringAlphabetString(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.StringAlphabet("ABCDEF", indices=["AAA", "AAB", "ABA", "ABB", "BAA", "BBB"])

    def test_index_size(self):
        self.assertEqual(3, self.alphabet.index_min_size)
        self.assertEqual(3, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"A", "B"}, self.alphabet.index_symbols)


class TestStringAlphabetStringNotMonotonic(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.StringAlphabet("ABCDEF", indices=["BBB", "AAA", "AAB", "ABA", "ABB", "BAA"])

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)

    def test_index_size(self):
        self.assertEqual(3, self.alphabet.index_min_size)
        self.assertEqual(3, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"A", "B"}, self.alphabet.index_symbols)


class TestStringAlphabetStringVariableSize(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.StringAlphabet("ABCDEF", indices=["AAA", "AABB", "ABAB", "ABBB", "BAAB", "BBBB"])

    def test_is_index_size_constant(self):
        self.assertFalse(self.alphabet.is_index_size_constant)

    def test_index_size(self):
        self.assertEqual(3, self.alphabet.index_min_size)
        self.assertEqual(4, self.alphabet.index_max_size)

    def test_index_symbols(self):
        self.assertEqual({"A", "B"}, self.alphabet.index_symbols)


class TestStringAlphabetStringNotMonotonicVariableSize(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.StringAlphabet("ABCDEF", indices=["BBBB", "AAA", "AABB", "ABAB", "ABBB", "BAAB"])

    def test_is_monotonic(self):
        self.assertFalse(self.alphabet.is_monotonic)

    def test_is_index_size_constant(self):
        self.assertFalse(self.alphabet.is_index_size_constant)

    def test_index_symbols(self):
        self.assertEqual({"A", "B"}, self.alphabet.index_symbols)


class TestAlphabetMixed(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.MixedAlphabet("ABCDEF", indices=["AAA", -1, "ABA", 7, "BAA", 22])

    def test_is_monotonic(self):
        with self.assertRaises(errors.IllegalAlphabetOperation):
            self.alphabet.is_monotonic


class TestBinaryAlphabet(TestAlphabet, unittest.TestCase):

    alphabet = alphabets.BinaryAlphabet()
