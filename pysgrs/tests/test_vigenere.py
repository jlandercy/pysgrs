import sys
import unittest

from pysgrs.tests.test_cypher import TestCypher
from pysgrs.cypher import VigenereCypher
from pysgrs import errors
from pysgrs import settings


class TestVigenereCypherSamllKey(TestCypher, unittest.TestCase):

    cypher = VigenereCypher(key="ABC")
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA"
    ]


class TestVigenereCypherMediumKey(TestCypher, unittest.TestCase):

    cypher = VigenereCypher(key="NATURELLEMENT")
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
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
