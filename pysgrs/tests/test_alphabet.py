import sys
import unittest

from pysgrs.interfaces import alphabet
from pysgrs import errors
from pysgrs import settings


class Alphabets(unittest.TestCase):

    def setUp(self):
        self.dummy = alphabet.GenericAlphabet(alphabet="ABC")
        self.dummyindices = alphabet.GenericAlphabet(alphabet="ABC", indices=[32, 71, -28])
        self.dummydict = alphabet.GenericAlphabet(alphabet={'B': 71, 'C': -28, 'A': 32})
        self.dummylist = alphabet.GenericAlphabet(alphabet=[('B', 71), ('C', -28), ('A', 32)])
        self.ASCII = alphabet.Alphabet()

    def test_dummy(self):
        self.assertEqual(self.dummy.alphabet, "ABC")
        self.assertEqual(self.dummy.indices, [0, 1, 2])
        self.assertEqual(self.dummy.encode("ABCCBA"), [0, 1, 2, 2, 1, 0])
        self.assertEqual(self.dummy.decode([0, 1, 2, 2, 1, 0]), "ABCCBA")

    def test_dummyindices(self):
        self.assertEqual(self.dummyindices.alphabet, "ABC")
        self.assertEqual(self.dummyindices.indices, [32, 71, -28])
        self.assertEqual(self.dummyindices.encode("ABCCBA"), [32, 71, -28, -28, 71, 32])
        self.assertEqual(self.dummyindices.decode([32, 71, -28, -28, 71, 32]), "ABCCBA")

    def test_dummylist(self):
        self.assertEqual(self.dummylist.alphabet, "ABC")
        self.assertEqual(self.dummylist.indices, [32, 71, -28])
        self.assertEqual(self.dummylist.encode("ABCCBA"), [32, 71, -28, -28, 71, 32])
        self.assertEqual(self.dummylist.decode([32, 71, -28, -28, 71, 32]), "ABCCBA")

    def test_dummydict(self):
        self.assertEqual(self.dummydict.alphabet, "ABC")
        self.assertEqual(self.dummydict.indices, [32, 71, -28])
        self.assertEqual(self.dummydict.encode("ABCCBA"), [32, 71, -28, -28, 71, 32])
        self.assertEqual(self.dummydict.decode([32, 71, -28, -28, 71, 32]), "ABCCBA")

    def test_ASCII(self):
        self.assertEqual(self.ASCII.alphabet, "".join([chr(x + 65) for x in range(26)]))
        self.assertEqual(self.ASCII.indices, list(range(26)))
        self.assertEqual(self.ASCII.encode("ABCCBA"), [0, 1, 2, 2, 1, 0])
        self.assertEqual(self.ASCII.decode([0, 1, 2, 2, 1, 0]), "ABCCBA")


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
