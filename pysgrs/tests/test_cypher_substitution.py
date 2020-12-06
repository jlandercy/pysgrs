import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import alphabets
from pysgrs import cyphers


class TestIdentityStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.RotationCypher(offset=0)
    cyphers = TestStreamCypher.sentences


class TestRotationStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.RotationCypher(offset=7)
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

    cypher = cyphers.RotationCypher(offset=-7)
    cyphers = [
        "TUVWXYZABCDEFGHIJKLMNOPQRS"
    ]


class TestCaesarStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.CaesarCypher()
    cyphers = [
        "DEFGHIJKLMNOPQRSTUVWXYZABC",
        "CBAZYXWVUTSRQPONMLKJIHGFED",
        "WKHTXLFNEURZQIRAMXPSVRYHUWKHODCBGRJ",
        "ZDOWCEDGQBPSKIRUTXLFNMLJVYHA",
        "MLYHGIRAQBPSKJUDEVTXLFNZDOWC",
        "JOLEMRFNVTXLCQBPSKWRYHAGZDUI",
        "VSKLQARIEODFNTXDUWCMXGJHPBYRZ",
        "KRZYHALQJOBTXLFNGDIWCHEUDVMXPS",
        "WKHILYHERALQJZLCDUGVMXPSTXLFNOB",
        "MDFNGDZVORYHPBELJVSKLQARITXDUWC",
        "SDFNPBERAZLWKILYHGRCHQOLTXRUMXJV",
        "Olyh dv li brx zhuh wr glh wrpruurz. Ohduq dv li brx zhuh wr olyh iruhyhu.",
        "Eh zkr brx duh dqg vdb zkdw brx ihho, ehfdxvh wkrvh zkr plqg grq’w pdwwhu dqg wkrvh zkr pdwwhu grq’w plqg.",
        "Li brx fdqqrw gr juhdw wklqjv, gr vpdoo wklqjv lq d juhdw zdb.",
        "Zlvh phq vshdn ehfdxvh wkhb kdyh vrphwklqj wr vdb; irrov ehfdxvh wkhb kdyh wr vdb vrphwklqj.",
        "Jdjd Jrxjrx Jrxjrx Gdgd",
        "Txdwuh mrxuqdxa krvwlohv vrqw soxv d fudlqguh txh plooh edlrqqhwwhv.", # This one is a bit ironic!
    ]


class TestReversedStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.ReversedCypher()
    cyphers = [
        "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    ]


class TestAlphabetStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.AlphabetCypher(
        alphabet=alphabets.StringAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                          indices="DEFGHIJKLMNOPQRSTUVWXYZABC")
    )
    cyphers = TestCaesarStreamCypher.cyphers


class TestPermutationIdentityStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.PermutationCypher()
    cyphers = TestStreamCypher.sentences


class TestPermutationStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.PermutationCypher(
        [
            10, 24,  8, 18, 15, 13,  1, 25,  9,
            22, 20,  6,  2,  0,  5,  3, 12, 21,
            19, 14, 16, 11,  7,  4, 23, 17
        ]
    )
    cyphers = [
        "KYISPNBZJWUGCAFDMVTOQLHEXR"
    ]


class TestPermutationStreamCypherRandom(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.PermutationCypher(auto=True)
    cyphers = []


class TestPermutationStreamCypherIdentity(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.PermutationCypher()
    cyphers = TestStreamCypher.sentences


class TestAffineStreamCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.AffineCypher()
    cyphers = [
        "INSXCHMRWBGLQVAFKPUZEJOTYD"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
