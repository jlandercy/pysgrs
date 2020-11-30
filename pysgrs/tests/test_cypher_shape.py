import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestTranspositionCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.TranspositionCypher()
    cyphers = [
        "AGMSYBHNTZCIOU DJPV EKQW FLRX"
   ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
