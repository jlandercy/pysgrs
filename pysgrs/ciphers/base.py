import sys
import base64
from urllib import parse

from pysgrs.interfaces import GenericBaseCipher
from pysgrs import errors
from pysgrs.settings import settings


class HexadecimalCipher(GenericBaseCipher):

    def encipher(self, s, **kwargs):
        return s.encode().hex().upper()

    def decipher(self, s, **kwargs):
        return bytes.fromhex(s).decode()


class Base16Cipher(GenericBaseCipher):

    def encipher(self, s, **kwargs):
        return base64.b16encode(s.encode()).decode()

    def decipher(self, s, **kwargs):
        return base64.b16decode(s.encode()).decode()


class Base32Cipher(GenericBaseCipher):

    def encipher(self, s, **kwargs):
        return base64.b32encode(s.encode()).decode()

    def decipher(self, s, **kwargs):
        return base64.b32decode(s.encode()).decode()


class Base64Cipher(GenericBaseCipher):

    def encipher(self, s, **kwargs):
        return base64.b64encode(s.encode()).decode()

    def decipher(self, s, **kwargs):
        return base64.b64decode(s.encode()).decode()


class Base85Cipher(GenericBaseCipher):

    def encipher(self, s, **kwargs):
        return base64.b85encode(s.encode()).decode()

    def decipher(self, s, **kwargs):
        return base64.b85decode(s.encode()).decode()


class URLQuoteCipher(GenericBaseCipher):

    def encipher(self, s, **kwargs):
        return parse.quote(s)

    def decipher(self, s, **kwargs):
        return parse.unquote(s)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
