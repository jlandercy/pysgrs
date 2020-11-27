import sys
import unittest

from pysgrs.tests.test_cypher import TestCypher
from pysgrs.cypher import Vigenere
from pysgrs import errors
from pysgrs import settings


class TestVigenereCypherSamllKey(TestCypher, unittest.TestCase):

    cypher = Vigenere(key="ABC")
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA"
    ]


class TestVigenereCypherLongKey(TestCypher, unittest.TestCase):

    cypher = Vigenere(key="NATURELLEMENT")
    cyphers = [
        "NBVXVJRSMVOYFAOIKIWEFZIBLS"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
