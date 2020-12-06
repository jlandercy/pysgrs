import sys

from pysgrs.settings import settings

from pysgrs import alphabets
from pysgrs import errors


class PolybeAlphabet(alphabets.IntegerAlphabet):

    def __init__(self):
        super().__init__(
            "ABCDEFGHIKLMNOPQRSTUVWXYZ",
            indices=[
                11, 12, 13, 14, 15,
                21, 22, 23, 24, 25,
                31, 32, 33, 34, 35,
                41, 42, 43, 44, 45,
                51, 52, 53, 54, 55,
            ]
        )


class MorseAlphabet(alphabets.StringAlphabet):

    def __init__(self):
        super().__init__({
            "A": "*-",     "B": "-***",   "C": "-*-*",
            "D": "-**",    "E": "*",      "F": "**-*",
            "G": "--*",    "H": "****",   "I": "**",
            "J": "*---",   "K": "-*-",    "L": "*-**",
            "M": "--",     "N": "-*",     "O": "---",
            "P": "*--*",   "Q": "--*-",   "R": "*-*",
            "S": "***",    "T": "-",      "U": "**-",
            "V": "***-",   "W": "*--",    "X": "-**-",
            "Y": "-*--",   "Z": "--**",
            "0": "-----",  "1": "*----",  "2": "**---",
            "3": "***--",  "4": "****-",  "5": "*****",
            "6": "-****",  "7": "--***",  "8": "---**",
            "9": "----*"
        })


class BaconAlphabet(alphabets.StringAlphabet):

    def __init__(self):
        super().__init__({
            "A": "aaaaa", "B": "aaaab", "C": "aaaba",
            "D": "aaabb", "E": "aabaa", "F": "aabab",
            "G": "aabba", "H": "aabbb", "I": "abaaa",
            "K": "abaab", "L": "ababa", "M": "ababb",
            "N": "abbaa", "O": "abbab", "P": "abbba",
            "Q": "abbbb", "R": "baaaa", "S": "baaab",
            "T": "baaba", "U": "baabb", "W": "babaa",
            "X": "babab", "Y": "babba", "Z": "babbb"
        })


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
