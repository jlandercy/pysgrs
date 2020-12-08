import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import ciphers


class TestVigenereStreamCypherSmallKey(TestStreamCypher, unittest.TestCase):

    cypher = ciphers.VigenereCypher(key="ABC")
    cyphers = [
        "ACEDFHGIKJLNMOQPRTSUWVXZYA",
        "ZZZWWWTTTQQQNNNKKKHHHEEEBB",
        "TIGQVKCLDRPYNGQXKWMQUOWGRUJEMCZZFOH",
        "WBNTADAEPYNRHGQRRWIDMJJISWGX",
        "JJXEEHOYPYNRHHTACUQVKCLYAMVZ",
        "GMKBKQCLUQVKZOAMQJTPXEYFWBTF",
        "SQJIOZOGDLBEKRWASVZKWDHGMZXOX",
        "HPYVFZIOILZSUJEKECFUBECTATLUNR",
        "TIGFJXECQXJPGXKZBTDTLUNRQVKCLNY",
        "JBEKECWTNOWGMZDIHUPIKNYQFRWASVZ",
        "PBEKNABPZWJVHGKVFFOAGNMKQVQRKWGT",
        "Ljxe bu ig aov yesg tp fif vonqrsqw. Mgasp at kf zqu xgrf vo mkvf hosgvft.",
        "Bf yhp aov crf cne uaz yhbv ypw ffgl, cgcbwsf vhpue xjo nkne foo’v mbvtft aof tiqsf yhp oauves foo’v mjpd.",
        "Ig aov eaopou fo htebv tiknhu, dp umbnl ujiois jp a htebv wba.",
        "Wjue ngn trebm bfeavue ujez jawg spoeujioi tp uaz; hopns cgcbwsf vhfa hbxe uq sba spoeujioi.",
        "Gbia Hquhqu Hquhqu Ecdb"
    ]


class TestVigenereStreamCypherMediumKey(TestStreamCypher, unittest.TestCase):

    cypher = ciphers.VigenereCypher(key="NATURELLEMENT")
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
