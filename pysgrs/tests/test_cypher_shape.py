import sys
import unittest

import numpy as np

from pysgrs.tests.test_cypher import TestShapeCypher
from pysgrs import ciphers
from pysgrs import toolbox


class TestTranspositionCypher(TestShapeCypher, unittest.TestCase):

    cypher = ciphers.TranspositionCipher(shape=(5, 5))
    cyphers = [
        "AFLQVBGMRWCHNSXDIOTYEKPUZ",
    ]


class TestColumnPermutationCypherIdentity(TestShapeCypher, unittest.TestCase):

    cypher = ciphers.ColumnPermutationCipher(shape=(5, 5), permutation=np.arange(5))
    cyphers = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestRowPermutationCypherIdentity(TestShapeCypher, unittest.TestCase):

    cypher = ciphers.RowPermutationCipher(shape=(5, 5), permutation=np.arange(5))
    cyphers = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestColumnCycleCypherIdentity(TestShapeCypher, unittest.TestCase):

    cypher = ciphers.ColumnCycleCipher(shape=(5, 5), permutation=np.zeros(5))
    cyphers = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestRowCycleCypherIdentity(TestShapeCypher, unittest.TestCase):

    cypher = ciphers.RowCycleCipher(shape=(5, 5), permutation=np.zeros(5))
    cyphers = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
