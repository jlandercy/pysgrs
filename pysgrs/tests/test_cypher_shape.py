import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestTranspositionCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.TranspositionCypher()
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


class TestColumnPermutationCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.ColumnPermutationCypher()
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


class TestRowPermutationCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.RowPermutationCypher()
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


class TestColumnCycleCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.ColumnCycleCypher()
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


class TestRowCycleCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.RowCycleCypher()
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
