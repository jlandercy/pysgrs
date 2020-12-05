import sys
import unittest

import numpy as np

from pysgrs.tests.test_cypher import TestShapeCypher
from pysgrs import cyphers
from pysgrs import toolbox


class TestTranspositionCypher(TestShapeCypher, unittest.TestCase):

    cypher = cyphers.TranspositionCypher(shape=(5, 5))
    cyphers = [
        "AFLQVBGMRWCHNSXDIOTYEKPUZ",
    ]


class TestColumnPermutationCypherIdentity(TestShapeCypher, unittest.TestCase):

    cypher = cyphers.ColumnPermutationCypher(shape=(5, 5), permutation=np.arange(5))
    cyphers = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestRowPermutationCypherIdentity(TestShapeCypher, unittest.TestCase):

    cypher = cyphers.RowPermutationCypher(shape=(5, 5), permutation=np.arange(5))
    cyphers = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestColumnCycleCypherIdentity(TestShapeCypher, unittest.TestCase):

    cypher = cyphers.ColumnCycleCypher(shape=(5, 5), permutation=np.zeros(5))
    cyphers = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestRowCycleCypherIdentity(TestShapeCypher, unittest.TestCase):

    cypher = cyphers.RowCycleCypher(shape=(5, 5), permutation=np.zeros(5))
    cyphers = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
