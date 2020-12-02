import sys
import unittest

import numpy as np

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestTranspositionCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.TranspositionCypher()
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


class TestColumnPermutationCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.ColumnPermutationCypher(shape=(11, 10), permutation=np.arange(10))
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


class TestRowPermutationCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.RowPermutationCypher(shape=(11, 10), permutation=np.arange(11))
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


class TestColumnCycleCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.ColumnCycleCypher(shape=(11, 10), permutation=np.arange(10))
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


class TestRowCycleCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.RowCycleCypher(shape=(11, 10), permutation=np.arange(10))
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
