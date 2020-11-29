import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs.cyphers import TranspositionCypher


class TestTranspositionCypher(TestStreamCypher, unittest.TestCase):

    cypher = TranspositionCypher()
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
   ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
