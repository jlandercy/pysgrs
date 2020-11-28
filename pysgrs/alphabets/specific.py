import sys

from pysgrs.settings import settings

from pysgrs.interfaces.alphabet import GenericAlphabet
from pysgrs import errors


class PolybeAlphabet(GenericAlphabet):

    def __init__(self):
        symbols = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        indices = [
            11, 12, 13, 14, 15,
            21, 22, 23, 24, 25,
            31, 32, 33, 34, 35,
            41, 42, 43, 44, 45,
            51, 52, 53, 54, 55,
        ]
        super().__init__(symbols, indices=indices)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
