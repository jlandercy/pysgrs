import sys

from pysgrs.interfaces import GenericBaseCypher
from pysgrs import errors
from pysgrs.settings import settings


class HexadecimalCypher(GenericBaseCypher):

    def cypher(self, s, **kwargs):
        pass

    def decypher(self, s, **kwargs):
        pass


class Base64Cypher(GenericBaseCypher):

    def cypher(self, s, **kwargs):
        pass

    def decypher(self, s, **kwargs):
        pass


class URLSafeCypher(GenericBaseCypher):

    def cypher(self, s, **kwargs):
        pass

    def decypher(self, s, **kwargs):
        pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
