import sys
import unittest

from pysgrs.tests.test_cypher import TestCypher
from pysgrs.cypher import KeyCypher, CaesarCypher
from pysgrs import errors
from pysgrs import settings


class TestKeyCypher(TestCypher, unittest.TestCase):

    cypher = KeyCypher(key="ABC")
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA"
    ]


class TestKeyRotationCyphersEquivalence(unittest.TestCase):

    def setUp(self):
        self.cypher = KeyCypher(key="D")
        self.caesar = CaesarCypher()

    def test_CaesarEquivalence(self):
        for sentence in TestCypher.sentences:
            self.assertEqual(self.cypher.cypher(sentence), self.caesar.cypher(sentence))


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
