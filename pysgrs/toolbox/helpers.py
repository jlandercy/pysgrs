import sys
import collections
import pathlib
import string
import unicodedata
import re

import numpy as np

from pysgrs.settings import settings


class Cleaner:

    _all_spaces = re.compile(r"\s+")
    _all_punctuations = re.compile('[%s]' % re.escape(string.punctuation))

    @staticmethod
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    @staticmethod
    def remove_punctuation(s):
        s = Cleaner._all_punctuations.sub(" ", s).strip()
        s = Cleaner._all_spaces.sub(" ", s).strip()
        return s


class FrequencyHelper:

    @staticmethod
    def counts(s):
        return collections.Counter(s)


class Book:

    def __init__(self, path):

        self._path = pathlib.Path(path)

    @property
    def path(self):
        return self._path



def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
