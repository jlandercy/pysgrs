import sys
import string
import unicodedata
import re

from pysgrs.settings import settings
from pysgrs import errors
from pysgrs.toolbox.shaper import Shaper


class Cleaner:
    pass


class AsciiCleaner(Cleaner):

    _all_spaces = re.compile(r"\s+")
    _all_punctuations = re.compile('[%s]' % re.escape(string.punctuation))
    _non_letters = re.compile(r"[^A-Za-z ]")

    @staticmethod
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    @staticmethod
    def remove_punctuation(s):
        s = AsciiCleaner._all_punctuations.sub(" ", s)
        s = AsciiCleaner._all_spaces.sub(" ", s)
        return s.strip()

    @staticmethod
    def remove_non_letters(s):
        s = AsciiCleaner._non_letters.sub("", s)
        return s

    @staticmethod
    def clean(s):
        s = AsciiCleaner.remove_punctuation(s)
        s = AsciiCleaner.strip_accents(s)
        s = AsciiCleaner.remove_non_letters(s)
        return s

    @staticmethod
    def normalize(s):
        s = AsciiCleaner.clean(s)
        s = s.replace(" ", "").upper()
        return s


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
