import sys
import collections
import pathlib
import string
import unicodedata
import re

import numpy as np
import pandas as pd

from pysgrs.settings import settings


class Cleaner:

    _all_spaces = re.compile(r"\s+")
    _all_punctuations = re.compile('[%s]' % re.escape(string.punctuation))
    _non_letters = re.compile(r"[^A-Za-z ]")

    @staticmethod
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    @staticmethod
    def remove_punctuation(s):
        s = Cleaner._all_punctuations.sub(" ", s)
        s = Cleaner._all_spaces.sub(" ", s)
        return s.strip()

    @staticmethod
    def clean(s):
        s = Cleaner.remove_punctuation(s)
        s = Cleaner.strip_accents(s)
        s = Cleaner._non_letters.sub("", s)
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

    def get_counts(self, n=3, counters=None):
        counters = counters or [collections.Counter() for i in range(n)]
        with self.path.open("r", encoding="utf-8") as file_handler:
            for line in file_handler:
                line = Cleaner.clean(line).upper()
                for word in line.split(" "):
                    m = len(word)
                    for k, counter in enumerate(counters):
                        counter.update(word[i:i+k+1] for i in range(m-k))
        return counters

    def get_frequencies(self, n=3):
        frequencies = []
        counters = self.get_counts(n=n)
        for counter in counters:
            df = pd.DataFrame.from_dict(dict(counter), orient="index", columns=["count"])
            df["frequency"] = df["count"]/df["count"].sum()
            df = df.sort_values("frequency", ascending=False)
            frequencies.append(df)
        return frequencies


def main():
    p = settings.resources/"books/fr/JulleVerne_20000LieuesSousLesMers.txt"
    cs = Book(p).get_frequencies()
    for c in cs:
        print(c)
    sys.exit(0)


if __name__ == "__main__":
    main()
