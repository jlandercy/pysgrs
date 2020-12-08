import sys
import unittest

import numpy as np

from pysgrs.tests.test_cipher import TestShapeCipher
from pysgrs import ciphers
from pysgrs import toolbox


class TestTranspositionCipher(TestShapeCipher, unittest.TestCase):

    cypher = ciphers.TranspositionCipher(shape=(5, 5))
    ciphertexts = [
        "AFLQVBGMRWCHNSXDIOTYEKPUZ",
    ]


class TestColumnPermutationCipherIdentity(TestShapeCipher, unittest.TestCase):

    cypher = ciphers.ColumnPermutationCipher(shape=(5, 5), permutation=np.arange(5))
    ciphertexts = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestRowPermutationCipherIdentity(TestShapeCipher, unittest.TestCase):

    cypher = ciphers.RowPermutationCipher(shape=(5, 5), permutation=np.arange(5))
    ciphertexts = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestColumnCycleCipherIdentity(TestShapeCipher, unittest.TestCase):

    cypher = ciphers.ColumnCycleCipher(shape=(5, 5), permutation=np.zeros(5))
    ciphertexts = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


class TestRowCycleCipherIdentity(TestShapeCipher, unittest.TestCase):

    cypher = ciphers.RowCycleCipher(shape=(5, 5), permutation=np.zeros(5))
    ciphertexts = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
