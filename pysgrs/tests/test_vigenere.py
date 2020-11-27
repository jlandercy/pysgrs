import sys
import unittest

from pysgrs.cypher import Vigenere
from pysgrs import errors
from pysgrs import settings


class TestCypher(unittest.TestCase):

    def setUp(self):
        self.cypher = Vigenere(key="MUSIQUE")

    def test_Cypher(self):
        pass


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
