import sys
import unittest

from pysgrs.cypher import RotationCypher, CaesarCypher
from pysgrs import errors
from pysgrs import settings


class TestCypher(unittest.TestCase):

    def setUp(self):
        self.identity = RotationCypher(offset=0)
        self.cypher = CaesarCypher()

    def test_cypher_illegalchar(self):
        with self.assertRaises(errors.IllegalCharacter):
            self.cypher.cypher("CaVECANEM")
        self.assertEqual(self.cypher.cypher("CaVE CANEM", strict=False, quite=True), "FDYH FDQHP")

    def test_cypher_caseinsensitive(self):
            self.assertEqual(self.cypher.cypher("CaVECANEM", strict=False), "FDYHFDQHP")

    def test_IdentityCypher(self):
        self.assertEqual(self.identity.alphabet.alphabet,
                         self.identity.decypher(self.identity.cypher(self.identity.alphabet.alphabet)))
        self.assertEqual(self.identity.cypher("CAVECANEM"), "CAVECANEM")

    def test_Cypher(self):
        self.assertEqual(self.cypher.alphabet.alphabet,
                         self.cypher.decypher(self.cypher.cypher(self.cypher.alphabet.alphabet)))
        self.assertEqual(self.cypher.cypher("CAVECANEM"), "FDYHFDQHP")


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
