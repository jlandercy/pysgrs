import sys
import base64
from urllib import parse

from pysgrs.interfaces import GenericBaseCypher
from pysgrs import errors
from pysgrs.settings import settings


class HexadecimalCypher(GenericBaseCypher):

    def cypher(self, s, **kwargs):
        return s.encode().hex()

    def decypher(self, s, **kwargs):
        return bytes.fromhex(s).decode()


class Base64Cypher(GenericBaseCypher):

    def cypher(self, s, **kwargs):
        return base64.b64encode(s.encode()).decode()

    def decypher(self, s, **kwargs):
        return base64.b64decode(s.encode()).decode()


class URLSafeCypher(GenericBaseCypher):

    def cypher(self, s, **kwargs):
        return parse.quote(s)

    def decypher(self, s, **kwargs):
        return parse.unquote(s)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
