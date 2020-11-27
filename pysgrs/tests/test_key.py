import sys
import unittest

from pysgrs.cypher import KeyCypher, CaesarCypher
from pysgrs import errors
from pysgrs import settings


class TestCypher(unittest.TestCase):

    def setUp(self):
        self.cypher = KeyCypher(key="ABC")

    def test_Reversible(self):
        self.assertEqual(self.cypher.decypher(self.cypher.cypher("ABC")), "ABC")

    def test_Cypher(self):
        self.assertEqual(self.cypher.cypher("ABC"), "ACE")


class TestEquivalence(unittest.TestCase):

    def setUp(self):
        self.cypher = KeyCypher(key="D")
        self.caesar = CaesarCypher()

    def test_CaesarEquivalence(self):
        self.assertEqual(self.cypher.cypher("ABC"), self.caesar.cypher("ABC"))


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
