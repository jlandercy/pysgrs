import sys

from pysgrs.settings import settings


class GenericException(Exception):
    pass


class BadParameter(GenericException):
    pass


class AlphabetException(GenericException):
    pass


class IllegalCharacter(AlphabetException):
    pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
