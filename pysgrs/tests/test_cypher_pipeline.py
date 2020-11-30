import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestPipelineCypherSimpleCase(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.PipelineCypher([cyphers.CaesarCypher(), cyphers.TranspositionCypher()])
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


class TestPipelineCypherEquivalenceCaeserRotation(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.PipelineCypher([cyphers.CaesarCypher(), cyphers.RotationCypher(offset=-3)])
    cyphers = TestStreamCypher.sentences


class TestPipelineCypherEquivalenceCaeserVigenere(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.PipelineCypher([cyphers.RotationCypher(offset=-3), cyphers.VigenereCypher(key="D")])
    cyphers = TestStreamCypher.sentences


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
