import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import ciphers


class TestPipelineCypherSimpleCase(TestStreamCypher, unittest.TestCase):

    cypher = ciphers.PipelineCipher([
        ciphers.CaesarCypher(),
        ciphers.TranspositionCypher()
    ])
    cyphers = [
        "DJPVBEKQWCFLRX GMSY HNTZ IOUA",
        "CWQKEBVPJDAUOI ZTNH YSMG XRLF",
        "WFQPUCKNISWBHERVKGTUARHRXRMYOJLZXHD",
        "ZDKLVDGIFYOQRNHWBUMACPTL ESXJ",
        "MRKTDLAJXOYQULWHBDFCGPEN ISVZ",
        "JFCWZONQRDLVBYUETPHIMXSA RLKG",
        "VRNCPSITMBKEXXYLODGRQDUJZAFWH",
        "KLXIDRQLWVZJFCMYONHXHBGEPATDUS",
        "WHJGTBKEZVX HRLML IACXF LLDPN YQUSO",
        "MZPSICDVBKT FOELX NRLQD GYJAU DHVRW",
        "SEKRTJDRICXVFALHR NZYQU PLHOM BWGLX",
        "Oihw  hyul  rOluh.ybwphih  hrrrd  i  x uubwr d guqrru vzlr x h  hhzd oy lu .vzlh",
        "Ed hh   pwhuzh ppwd  hkowldkwpz d,kqwrwlkdw rgwvhqrq ev hhug gbhhgu  .b rf r zg rvxdzqdkr xd xk’qrq  bivrwg ’",
        "Ld krwqwiqjl k   quqvldzbrhjpq drwdvdjjbx w,ovu. g  o h frwg ld",
        "Zsvyq dkbjlhhhjixd .vd   rvyv hnwvwrhhr   krro  p pehp vwwh hhbhv krw qf wdeh k  dkkbhbvl vxdl;f dq",
        "JJxjddr rgjxJxddjr   rxG"
    ]


class TestPipelineCypherComplexCase(TestStreamCypher, unittest.TestCase):

    cypher = P = ciphers.PipelineCipher([
        ciphers.CaesarCypher(),
        ciphers.VigenereCypher(key="NAPOLEON"),
        ciphers.TranspositionCypher()
    ])
    cyphers = [
        "QXAKOEXUKCUYFI UMFC SCGN MCUN",
        "PKBZRBITXDPHCT NTAL JHZU BFLS",
        "JTBEHQKAMGWOWRFGZTHUNVVRIGZMZYPNXUH",
        "MRVAIDTMTYDDFYWKBHQONEGZ IGXW",
        "ZFVIQLNNLONDIWLVBQJQRERB MGVM",
        "WTNLMOAUFDAIPJJSTCLWXMFO VZKT",
        "IFYRCSVXABZRLINZOQKFBSHXKETWU",
        "XZIXQRDPKVOWTNBMOALLSQTSAEHDHW",
        "JVUVGPKRDJX WEZXA WAPBT WAQDY CEUFS",
        "ZNAHVQDIFYT UBSWM BRYUR RNWOF HVVEA",
        "FSVGGXDEMQXIUNZSG BZLUI AAUCX FKGYB",
        "Bvvh  hlhl  vZzjh.nojdltv  vreer  x  m hhfhf o gudfvf znag k l  svnd cm zy .kmyu",
        "Rq hw   aahuzw ddhh  wzckwookdo r,vuafjyyrh vukiudcb pj uuug kfluth  .f ft e zv fjkqmqdzf kq kk’ffb  ovvglu ’",
        "Yr yrjehidnw x   diuklqdqruxdf rflqioxwoi w,sgu. u  c w jclt pr",
        "Mfvyf dkbylhwwxims .ks   gjmk vbkjhfssf   vcvz  a aplt zaal llpvj yfk et jqsu x  qxxouoiy ikql;s qq",
        "WUxnddv fvylYkrrwf   eiT"
    ]


class TestPipelineCypherVigenereSquared(TestStreamCypher, unittest.TestCase):

    cypher = P = ciphers.PipelineCipher([
        ciphers.VigenereCypher(key="FIRST"),
        ciphers.VigenereCypher(key="SECOND"),
    ])
    cyphers = [
        "XNVJKNGCCQCWVJJILLCQBRASJI",
        "WKQCBCTNLXHZWIGDECRDMAHXMJ",
        "QTXWAQCFVYGHWBJQEOWMZKZZCCRJQWWKWUM",
        "TMEZFJAYHFEAQBJKLOSZRFMBDEOC",
        "GUOKJNOSHFEAQCMTWMARPYORLUDE",
        "DXBHPWCFMXMTIJTFKBDLCABYHJBK",
        "PBAOTFOAVSSNTMPTMNJGBZKZXHFTB",
        "EAPBKFIIASQBDEXDYUPQGAFMLBTZRL",
        "QTXLODEWIEAYPSDSVLNPQQQKBDSHPHV",
        "GMVQJIWNFVNPVUWBBMZEPJBJQZEFWPW",
        "MMVQSGBJRDAEQBDOZXYWLJPDBDYWOQDE",
        "Iuok ga ia svm hnnz mj xsb akqjcayb. Qaxdg gy qf tib opaa oh gcfb mkvzgnb.",
        "Yq pnu gop uyw lwz ntt qrxa usp qnoq, gazmnyk bhjml osx idgy xyk’a ieoenb fsz qthyk ehj ghlenn yhi’n wfuz.",
        "Fr rua kaihvl ox cmxvn depjkn, ox crfhi faotos dh h ycnwo pvs.",
        "Tulk smn njlsv kaxtpmo qoac cleo xtibfaoto tj mhq; qxkgl wymxboi osni mfrb fh ygg sjgllsrjb.",
        "Dmzg Mwubib Yzdcjn Yunx",
        "Ngtzxm jjoyfldt chnnsilo wjyc zqzo x okgovdmy xmp vegez vkfvjrzecox."
    ]


class TestPipelineCypherVigenereSquaredIsVigenere(TestStreamCypher, unittest.TestCase):

    cypher = P = ciphers.PipelineCipher([
        ciphers.VigenereCypher(key="BOB"),
        ciphers.VigenereCypher(key="BOBETTE"),
    ])
    cyphers = [
        "CDEILZLWXLCFGFQEFWMAZXYZDG",
    ]


class TestPipelineCypherVigenereSquaredIsVigenereCrossCheck(TestStreamCypher, unittest.TestCase):

    cypher = ciphers.VigenereCypher(key="CCCFHUFPPCSUUSCPPFUHF")
    cyphers = TestPipelineCypherVigenereSquaredIsVigenere.cyphers


class TestPipelineCypherEquivalenceCaeserRotation(TestStreamCypher, unittest.TestCase):

    cypher = ciphers.PipelineCipher([ciphers.CaesarCypher(), ciphers.RotationCypher(offset=-3)])
    cyphers = TestStreamCypher.sentences


class TestPipelineCypherEquivalenceCaeserVigenere(TestStreamCypher, unittest.TestCase):

    cypher = ciphers.PipelineCipher([ciphers.RotationCypher(offset=-3), ciphers.VigenereCypher(key="D")])
    cyphers = TestStreamCypher.sentences


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
