import sys
import unittest

from pysgrs.tests.test_cypher import TestCypher
from pysgrs.cypher import RotationCypher, CaesarCypher, ReversedCypher
from pysgrs import errors
from pysgrs import settings


class TestIdentityCypher(TestCypher, unittest.TestCase):

    cypher = RotationCypher(offset=0)
    cyphers = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ]


class TestRotationCypher(TestCypher, unittest.TestCase):

    cypher = RotationCypher(offset=7)
    cyphers = [
        "HIJKLMNOPQRSTUVWXYZABCDEFG"
    ]


class TestNegativeRotationCypher(TestCypher, unittest.TestCase):

    cypher = RotationCypher(offset=-7)
    cyphers = [
        "TUVWXYZABCDEFGHIJKLMNOPQRS"
    ]


class TestCaesarCypher(TestCypher, unittest.TestCase):

    cypher = CaesarCypher()
    cyphers = [
        "DEFGHIJKLMNOPQRSTUVWXYZABC"
    ]


class TestReversedCypher(TestCypher, unittest.TestCase):

    cypher = ReversedCypher()
    cyphers = [
        "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
