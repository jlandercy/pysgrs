import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestVigenereStreamCypherSmallKey(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.VigenereCypherNaturalAlphabet(key="ABC")
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA"
    ]


class TestVigenereStreamCypherMediumKey(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.VigenereCypherNaturalAlphabet(key="NATURELLEMENT")
    cyphers = [
        "NBVXVJRSMVOYFAOIKIWEFZIBLS",
        "MYQQMYEDVCTBGZLDDZLRQIPGOT",
        "GHXKLMNVFDSJGSOQDLQADSHIEMUEEUQCOZK",
        "JAENQFLORKQCASOKKLMNVNUKFORX",
        "WIOYUJZIRKQCATRTVJUFTGWANEGZ",
        "TLBVASNVWCYVSAYFJYXZGIJHJTEF",
        "FPACEBZQFXEPDDUTLKDUFHSIZRIOP",
        "UOPPVBTYKXCDNVCDXRJEKINVNLWUFJ",
        "GHXZZZPMSJMAZJISUIHDUYYTDNVCDFP",
        "WAVEUEHDPAZRFLBBAJTSTRJSSJHAKNQ",
        "CAVEDCMZBIMGASIOYUSKPRXMDNBRCOXW",
        "Yioy rw tq cay jxee mi ump esysekbw. Eyrvy lw uj lhh wxlv xz wmhi sheeoyi.",
        "Oe pbf czf edi ngq sts nlle cay sxrl, uytefdi flblr wai dmyo har’g fntmyi eyo xtsfx jhh grxepv psa’m zigx.",
        "Vf ril glyrax qh trxuk xstrsw, qh fmtfc xstrsw vg n gkyrx hlc.",
        "Jily diy dtqex urctoji esik lnor shgvxstrs xb lny; yifpd mioehlr tayp llgi fs ftl shgvxstrs."
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
