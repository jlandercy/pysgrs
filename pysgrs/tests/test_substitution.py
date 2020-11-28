import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs.cyphers import RotationCypher, CaesarCypher, ReversedCypher, PermutationCypher, AffineCypher


class TestIdentityStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = RotationCypher(offset=0)
    cyphers = TestStreamCypher.sentences


class TestRotationStreamCypher(TestStreamCypher, unittest.TestCase):

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


class TestNegativeRotationStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = RotationCypher(offset=-7)
    cyphers = [
        "TUVWXYZABCDEFGHIJKLMNOPQRS"
    ]


class TestCaesarStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = CaesarCypher()
    cyphers = [
        "DEFGHIJKLMNOPQRSTUVWXYZABC"
    ]


class TestReversedStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = ReversedCypher()
    cyphers = [
        "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    ]


class TestPermutationIdentityStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = PermutationCypher()
    cyphers = TestStreamCypher.sentences


class TestPermutationStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = PermutationCypher([10, 24,  8, 18, 15, 13,  1, 25,  9,
                                22, 20,  6,  2,  0,  5,  3, 12, 21,
                                19, 14, 16, 11,  7,  4, 23, 17])
    cyphers = [
        "KYISPNBZJWUGCAFDMVTOQLHEXR"
    ]


class TestAffineStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = AffineCypher()
    cyphers = [
        "INSXCHMRWBGLQVAFKPUZEJOTYD"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
