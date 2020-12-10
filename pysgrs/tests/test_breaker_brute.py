import sys
import unittest

import pandas as pd

from pysgrs import interfaces
from pysgrs import ciphers
from pysgrs import breakers
from pysgrs import scores
from pysgrs.tests.test_breaker import TestBruteForceBreaker


class TestBruteForceBreakerOnRotationCipher(TestBruteForceBreaker, unittest.TestCase):

    breaker = breakers.BruteForceBreaker(
        interfaces.CipherFactory(ciphers.RotationCipher, offset=range(0, 27)),
        scores.MultiNGramScore().ngrams[2]
    )
    ciphers = interfaces.CipherFactory(ciphers.RotationCipher, offset=[3, 7, 12, 16, 21, 24])


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
