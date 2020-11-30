import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestHexadecimalCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.HexadecimalCypher()
    cyphers = [
        "4142434445464748494a4b4c4d4e4f505152535455565758595a"
    ]


class TestBase64Cypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.Base64Cypher()
    cyphers = [
        "QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVo="
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
