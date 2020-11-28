import sys
import unittest

from pysgrs.tests.test_cypher import TestCypher
from pysgrs.cypher import RotationCypher, CaesarCypher, ReversedCypher
from pysgrs import errors
from pysgrs import settings


class TestIdentityCypher(TestCypher, unittest.TestCase):

    cypher = RotationCypher(offset=0)
    cyphers = TestCypher.sentences


class TestRotationCypher(TestCypher, unittest.TestCase):

    cypher = RotationCypher(offset=7)
    cyphers = [
        "HIJKLMNOPQRSTUVWXYZABCDEFG",
        "GFEDCBAZYXWVUTSRQPONMLKJIH",
        "AOLXBPJRIYVDUMVEQBTWZVCLYAOLSHGFKVN",
        "DHSAGIHKUFTWOMVYXBPJRQPNZCLE",
        "QPCLKMVEUFTWONYHIZXBPJRDHSAG",
        "NSPIQVJRZXBPGUFTWOAVCLEKDHYM",
        "ZWOPUEVMISHJRXBHYAGQBKNLTFCVD",
        "OVDCLEPUNSFXBPJRKHMAGLIYHZQBTW",
        "AOLMPCLIVEPUNDPGHYKZQBTWXBPJRSF",
        "QHJRKHDZSVCLTFIPNZWOPUEVMXBHYAG",
        "WHJRTFIVEDPAOMPCLKVGLUSPXBVYQBNZ",
        "Spcl hz pm fvb dlyl av kpl avtvyyvd. Slhyu hz pm fvb dlyl av spcl mvylcly.",
        "Il dov fvb hyl huk zhf doha fvb mlls, iljhbzl aovzl dov tpuk kvu’a thaaly huk aovzl dov thaaly kvu’a tpuk.",
        "Pm fvb jhuuva kv nylha aopunz, kv zthss aopunz pu h nylha dhf.",
        "Dpzl tlu zwlhr iljhbzl aolf ohcl zvtlaopun av zhf; mvvsz iljhbzl aolf ohcl av zhf zvtlaopun.",
    ]


class TestNegativeRotationCypher(TestCypher, unittest.TestCase):

    cypher = RotationCypher(offset=-7)
    cyphers = [
        "TUVWXYZABCDEFGHIJKLMNOPQRS"
    ]


class TestCaesarCypher(TestCypher, unittest.TestCase):

    cypher = CaesarCypher()
    cyphers = [
        "DEFGHIJKLMNOPQRSTUVWXYZABC"
    ]


class TestReversedCypher(TestCypher, unittest.TestCase):

    cypher = ReversedCypher()
    cyphers = [
        "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
