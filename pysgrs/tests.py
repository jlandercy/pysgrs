import sys
import unittest

from pysgrs import base
from pysgrs import errors
from pysgrs import settings


class Settings(unittest.TestCase):

    def test_NameSpace(self):
        self.assertIsInstance(settings.settings, settings.SimpleNamespace)

    def test_RequiredSettings(self):
        self.assertTrue({'package', 'resources', 'uuid4'}.issubset(settings.settings.__dict__))


class Alphabets(unittest.TestCase):

    def setUp(self):
        self.dummy = base.GenericAlphabet(alphabet="ABC")
        self.dummyindices = base.GenericAlphabet(alphabet="ABC", indices=[32, 71, -28])
        self.dummydict = base.GenericAlphabet(alphabet={'B': 71, 'C': -28, 'A': 32})
        self.dummylist = base.GenericAlphabet(alphabet=[('B', 71), ('C', -28), ('A', 32)])
        self.ASCII = base.Alphabet()

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


class Cyphers(unittest.TestCase):

    def setUp(self):
        self.identity = base.Cypher()
        self.ceasar = base.Cypher(offset=3)

    def test_cypher_illegalchar(self):
        with self.assertRaises(errors.IllegalCharacter):
            self.ceasar.cypher("CAVE CANEM")
            self.ceasar.cypher("CaVECANEM")
        self.assertEqual(self.ceasar.cypher("CaVE CANEM", strict=False, quite=True), "FDYH FDQHP")

    def test_cypher_caseinsensitive(self):
            self.assertEqual(self.ceasar.cypher("CaVECANEM", strict=False), "FDYHFDQHP")

    def test_IdentityCypher(self):
        self.assertEqual(self.identity.alphabet.alphabet,
                         self.identity.decypher(self.identity.cypher(self.identity.alphabet.alphabet)))
        self.assertEqual(self.identity.cypher("CAVECANEM"), "CAVECANEM")

    def test_CeasarCypher(self):
        self.assertEqual(self.ceasar.alphabet.alphabet,
                         self.ceasar.decypher(self.ceasar.cypher(self.ceasar.alphabet.alphabet)))
        self.assertEqual(self.ceasar.cypher("CAVECANEM"), "FDYHFDQHP")


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
