import sys

from pysgrs.settings import settings


class GenericException(Exception):
    pass


class IllegalCharacter(GenericException):
    pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
