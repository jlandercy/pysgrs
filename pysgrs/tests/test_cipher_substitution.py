import sys
import unittest

from pysgrs.tests.test_cipher import TestStreamCipher
from pysgrs import alphabets
from pysgrs import ciphers


class TestIdentityStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.RotationCipher(offset=0)
    ciphertexts = TestStreamCipher.plaintexts


class TestRotationStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.RotationCipher(offset=7)
    ciphertexts = [
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


class TestNegativeRotationStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.RotationCipher(offset=-7)
    ciphertexts = [
        "TUVWXYZABCDEFGHIJKLMNOPQRS"
    ]


class TestCaesarStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.CaesarCipher()
    ciphertexts = [
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


class TestReversedStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.ReversedCipher()
    ciphertexts = [
        "ZYXWVUTSRQPONMLKJIHGFEDCBA"
    ]


class TestAlphabetStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.AlphabetCipher(
        alphabet=alphabets.StringAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                          indices="DEFGHIJKLMNOPQRSTUVWXYZABC")
    )
    ciphertexts = TestCaesarStreamCipher.ciphertexts


class TestPermutationIdentityStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.PermutationCipher()
    ciphertexts = TestStreamCipher.plaintexts


class TestPermutationStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.PermutationCipher(
        [
            10, 24,  8, 18, 15, 13,  1, 25,  9,
            22, 20,  6,  2,  0,  5,  3, 12, 21,
            19, 14, 16, 11,  7,  4, 23, 17
        ]
    )
    ciphertexts = [
        "KYISPNBZJWUGCAFDMVTOQLHEXR"
    ]


class TestPermutationStreamCipherRandom(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.PermutationCipher(auto=True)
    ciphertexts = []


class TestPermutationStreamCipherIdentity(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.PermutationCipher()
    ciphertexts = TestStreamCipher.plaintexts


class TestAffineStreamCipher(TestStreamCipher, unittest.TestCase):

    cipher = ciphers.AffineCipher()
    ciphertexts = [
        "INSXCHMRWBGLQVAFKPUZEJOTYD"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
