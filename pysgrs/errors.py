import sys

from pysgrs.settings import settings


class GenericException(Exception):
    pass


class IllegalParameter(GenericException):
    pass


class AlphabetException(GenericException):
    pass


class CipherException(GenericException):
    pass


class IllegalAlphabetParameter(IllegalParameter):
    pass


class IllegalAlphabetOperation(GenericException):
    pass


class IllegalAlphabetIndex(AlphabetException):
    pass


class AmbiguousAlphabetIndex(AlphabetException):
    pass


class IllegalCipherParameter(IllegalParameter):
    pass


class IllegalCipherOperation(GenericException):
    pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
