import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestBaseCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.VigenereCypher(key="ABC")
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
