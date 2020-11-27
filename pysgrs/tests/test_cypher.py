import sys
import unittest

from pysgrs.cypher import Caesar
from pysgrs import errors
from pysgrs import settings


class Cyphers(unittest.TestCase):

    def setUp(self):
        self.identity = Caesar(offset=0)
        self.ceasar = Caesar(offset=3)

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
