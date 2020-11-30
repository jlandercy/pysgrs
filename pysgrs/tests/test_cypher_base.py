import sys
import unittest

from pysgrs.tests.test_cypher import TestStreamCypher
from pysgrs import cyphers


class TestBase16Cypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.Base16Cypher()
    cyphers = [
        "4142434445464748494A4B4C4D4E4F505152535455565758595A",
        "5A595857565554535251504F4E4D4C4B4A494847464544434241",
        "544845515549434B42524F574E464F584A554D50534F5645525448454C415A59444F47",
        "57414C545A4241444E594D5048464F52515549434B4A494753564558",
        "4A49564544464F584E594D50484752414253515549434B57414C545A",
        "474C49424A4F434B535155495A4E594D5048544F5645584457415246",
        "535048494E584F46424C41434B51554152545A4A554447454D59564F57",
        "484F57564558494E474C59515549434B444146545A45425241534A554D50",
        "54484546495645424F58494E4757495A415244534A554D50515549434B4C59",
        "4A41434B444157534C4F56454D59424947535048494E584F4651554152545A",
        "5041434B4D59424F585749544846495645444F5A454E4C4951554F524A554753",
        "4C69766520617320696620796F75207765726520746F2064696520746F6D6F72726F772E204C6561726E20617320696620796F75207765726520746F206C69766520666F72657665722E",
        "42652077686F20796F752061726520616E6420736179207768617420796F75206665656C2C20626563617573652074686F73652077686F206D696E6420646F6EE2809974206D617474657220616E642074686F73652077686F206D617474657220646F6EE2809974206D696E642E",
        "496620796F752063616E6E6F7420646F206772656174207468696E67732C20646F20736D616C6C207468696E677320696E2061206772656174207761792E",
        "57697365206D656E20737065616B20626563617573652074686579206861766520736F6D657468696E6720746F207361793B20666F6F6C7320626563617573652074686579206861766520746F2073617920736F6D657468696E672E",
        "4761676120476F75676F7520476F75676F752044616461"
    ]


class TestHexadecimalCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.HexadecimalCypher()
    cyphers = TestBase16Cypher.cyphers


class TestBase32Cypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.Base32Cypher()
    cyphers = [
        "IFBEGRCFIZDUQSKKJNGE2TSPKBIVEU2UKVLFOWCZLI======",
        "LJMVQV2WKVKFGUSRKBHU4TKMJNFESSCHIZCUIQ2CIE======",
        "KREEKUKVJFBUWQSSJ5LU4RSPLBFFKTKQKNHVMRKSKREEKTCBLJMUIT2H",
        "K5AUYVC2IJAUITSZJVIEQRSPKJIVKSKDJNFESR2TKZCVQ===",
        "JJEVMRKEIZHVQTSZJVIEQR2SIFBFGUKVJFBUWV2BJRKFU===",
        "I5GESQSKJ5BUWU2RKVEVUTSZJVIEQVCPKZCVQRCXIFJEM===",
        "KNIEQSKOLBHUMQSMIFBUWUKVIFJFIWSKKVCEORKNLFLE6VY=",
        "JBHVOVSFLBEU4R2MLFIVKSKDJNCECRSULJCUEUSBKNFFKTKQ",
        "KREEKRSJKZCUET2YJFHEOV2JLJAVERCTJJKU2UCRKVEUGS2MLE======",
        "JJAUGS2EIFLVGTCPKZCU2WKCJFDVGUCIJFHFQT2GKFKUCUSULI======",
        "KBAUGS2NLFBE6WCXJFKEQRSJKZCUIT22IVHEYSKRKVHVESSVI5JQ====",
        "JRUXMZJAMFZSA2LGEB4W65JAO5SXEZJAORXSAZDJMUQHI33NN5ZHE33XFYQEYZLBOJXCAYLTEBUWMIDZN52SA53FOJSSA5DPEBWGS5TFEBTG64TFOZSXELQ=",
        "IJSSA53IN4QHS33VEBQXEZJAMFXGIIDTMF4SA53IMF2CA6LPOUQGMZLFNQWCAYTFMNQXK43FEB2GQ33TMUQHO2DPEBWWS3TEEBSG63XCQCMXIIDNMF2HIZLSEBQW4ZBAORUG643FEB3WQ3ZANVQXI5DFOIQGI33O4KAJS5BANVUW4ZBO",
        "JFTCA6LPOUQGGYLONZXXIIDEN4QGO4TFMF2CA5DINFXGO4ZMEBSG6IDTNVQWY3BAORUGS3THOMQGS3RAMEQGO4TFMF2CA53BPEXA====",
        "K5UXGZJANVSW4IDTOBSWC2ZAMJSWGYLVONSSA5DIMV4SA2DBOZSSA43PNVSXI2DJNZTSA5DPEBZWC6J3EBTG633MOMQGEZLDMF2XGZJAORUGK6JANBQXMZJAORXSA43BPEQHG33NMV2GQ2LOM4XA====",
        "I5QWOYJAI5XXKZ3POUQEO33VM5XXKICEMFSGC==="
    ]


class TestBase64Cypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.Base64Cypher()
    cyphers = [
        "QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVo=",
        "WllYV1ZVVFNSUVBPTk1MS0pJSEdGRURDQkE=",
        "VEhFUVVJQ0tCUk9XTkZPWEpVTVBTT1ZFUlRIRUxBWllET0c=",
        "V0FMVFpCQUROWU1QSEZPUlFVSUNLSklHU1ZFWA==",
        "SklWRURGT1hOWU1QSEdSQUJTUVVJQ0tXQUxUWg==",
        "R0xJQkpPQ0tTUVVJWk5ZTVBIVE9WRVhEV0FSRg==",
        "U1BISU5YT0ZCTEFDS1FVQVJUWkpVREdFTVlWT1c=",
        "SE9XVkVYSU5HTFlRVUlDS0RBRlRaRUJSQVNKVU1Q",
        "VEhFRklWRUJPWElOR1dJWkFSRFNKVU1QUVVJQ0tMWQ==",
        "SkFDS0RBV1NMT1ZFTVlCSUdTUEhJTlhPRlFVQVJUWg==",
        "UEFDS01ZQk9YV0lUSEZJVkVET1pFTkxJUVVPUkpVR1M=",
        "TGl2ZSBhcyBpZiB5b3Ugd2VyZSB0byBkaWUgdG9tb3Jyb3cuIExlYXJuIGFzIGlmIHlvdSB3ZXJlIHRvIGxpdmUgZm9yZXZlci4=",
        "QmUgd2hvIHlvdSBhcmUgYW5kIHNheSB3aGF0IHlvdSBmZWVsLCBiZWNhdXNlIHRob3NlIHdobyBtaW5kIGRvbuKAmXQgbWF0dGVyIGFuZCB0aG9zZSB3aG8gbWF0dGVyIGRvbuKAmXQgbWluZC4=",
        "SWYgeW91IGNhbm5vdCBkbyBncmVhdCB0aGluZ3MsIGRvIHNtYWxsIHRoaW5ncyBpbiBhIGdyZWF0IHdheS4=",
        "V2lzZSBtZW4gc3BlYWsgYmVjYXVzZSB0aGV5IGhhdmUgc29tZXRoaW5nIHRvIHNheTsgZm9vbHMgYmVjYXVzZSB0aGV5IGhhdmUgdG8gc2F5IHNvbWV0aGluZy4=",
        "R2FnYSBHb3Vnb3UgR291Z291IERhZGE="
    ]


class TestBase85Cypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.Base85Cypher()
    cyphers = [
        "K|(`BMMg(RNlHshO-@fxQBqS>RaRG6Sy}",
        "T3J|ER#j9}Qc+M(PEAZpN=ZmZMnyzJLO}",
        "R7gcpRY^ljLQ+pxPDW2yN>xozQ%_b!QdCGqOhH;%L{CQ",
        "S3yivT0%iYPFYP*NJdXmQB_GpOG-&cQ&vS-",
        "N=a5lL`F|oPFYP*NJmmZLQ_#yNkdClK}=Ly",
        "M@&gVN>4*eQ&Ck(T25I_P)JlyRz+AuS3y!n",
        "Q&31rPFPPyLQFwJOHoxpQdC+>RYXTcO<7h?R{",
        "NKaQ*MOaBrM@(5!RY^ljL_tPWT17%qK~qXqO;7",
        "R7gceNmfNdPgqG#M^{N&K~h9hN>xozQB_GpOH5e",
        "N<l+QL_t?mOixxtO<6)oM^jKpNlsW#Mp0EkQdC+",
        "P(edWO<6)uSXW6@NJdFkMMO_pMNUjfQB_Y;N>xWw",
        "OlfvyAYpSLX=WgKZ*?GdWpZU8bZ;PJX=NaEZ*6aKa&LDoAWUUpa&91Db0BGEAbD?fAa`YQWgv8KAZ%%NWgup6a%Fa9axM",
        "LS-O#Xm22SZ*?GHa%CW4Ze$>HVR;~TXkm09d2e+fW@Tk;EFfZKV_|i3Wgv8DZ*yfJcW7@QZE0>~AY^ZD;((cSAZ=lEbY*fNVQyp~bZBpLWgvHGZy;@9baZ8MAY^ZD;((cSAZ=-GWG(",
        "NoF8<Z*?GJVQy}3bRcAJAZK!AVRRsLXlZU|b1WcaZy<ARVQg$5bZBXAXLBHFZXjVGXL4m>bRc(Oc`g",
        "S7~!)AZ=xCAaihKVQU~_Wn*D=b7dfOXk~dIXkm6`AaieRWprq1Zf78LZy<AFc{?CxZ*OdKAYx@>VRdt5AarPDc_3(Ec4Z)RZy<AFc_4FdZDn+5X>MmO",
        "M`34SAV+U?XK!^NM{jj!Z*?F<VPs("
    ]


class URLSafeCypher(TestStreamCypher, unittest.TestCase):

    cypher = cyphers.URLQuoteCypher()
    cyphers = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBA",
        "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
        "WALTZBADNYMPHFORQUICKJIGSVEX",
        "JIVEDFOXNYMPHGRABSQUICKWALTZ",
        "GLIBJOCKSQUIZNYMPHTOVEXDWARF",
        "SPHINXOFBLACKQUARTZJUDGEMYVOW",
        "HOWVEXINGLYQUICKDAFTZEBRASJUMP",
        "THEFIVEBOXINGWIZARDSJUMPQUICKLY",
        "JACKDAWSLOVEMYBIGSPHINXOFQUARTZ",
        "PACKMYBOXWITHFIVEDOZENLIQUORJUGS",
        "Live%20as%20if%20you%20were%20to%20die%20tomorrow.%20Learn%20as%20if%20you%20were%20to%20live%20forever.",
        "Be%20who%20you%20are%20and%20say%20what%20you%20feel%2C%20because%20those%20who%20mind%20don%E2%80%99t%20matter%20and%20those%20who%20matter%20don%E2%80%99t%20mind.",
        "If%20you%20cannot%20do%20great%20things%2C%20do%20small%20things%20in%20a%20great%20way.",
        "Wise%20men%20speak%20because%20they%20have%20something%20to%20say%3B%20fools%20because%20they%20have%20to%20say%20something.",
        "Gaga%20Gougou%20Gougou%20Dada"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
