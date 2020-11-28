import sys

from pysgrs.settings import settings


class GenericException(Exception):
    pass


class BadParameter(GenericException):
    pass


class AlphabetException(GenericException):
    pass


class IllegalOperation(GenericException):
    pass


class IllegalIndexer(AlphabetException):
    pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
