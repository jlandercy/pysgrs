import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestHexadecimalCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.HexadecimalCypher()
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA"
    ]


class TestBase64Cypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.Base64Cypher()
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA"
    ]


class URLSafeCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.URLSafeCypher()
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
