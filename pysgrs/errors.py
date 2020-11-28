import sys

from pysgrs.settings import settings


class GenericException(Exception):
    pass


class IllegalParameter(GenericException):
    pass


class AlphabetException(GenericException):
    pass


class CypherException(GenericException):
    pass


class IllegalAlphabetParameter(IllegalParameter):
    pass


class IllegalAlphabetOperation(GenericException):
    pass


class IllegalAlphabetIndexer(AlphabetException):
    pass


class IllegalAlphabetIndexerType(AlphabetException):
    pass


class IllegalAlphabetSymbol(IllegalAlphabetIndexer):
    pass


class IllegalAlphabetIndex(IllegalAlphabetIndexer):
    pass


class IllegalCypherParameter(IllegalParameter):
    pass


class IllegalCypherOperation(GenericException):
    pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
