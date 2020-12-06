import sys
import collections
import pathlib
import unicodedata

import numpy as np

from pysgrs.settings import settings


class Cleaner:

    @staticmethod
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


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
