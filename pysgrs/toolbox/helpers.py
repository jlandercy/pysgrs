import sys
import collections
from collections.abc import Iterable
import pathlib
import string
import unicodedata
import re

import numpy as np
import pandas as pd

from pysgrs.settings import settings
from pysgrs import errors


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


class FrequencyAnalysis:

    @staticmethod
    def get_counts(source=None, n=3):
        counters = [collections.Counter() for i in range(n)]
        # Parse arguments:
        if source is None:
            return counters
        if isinstance(source, pathlib.Path):
            with pathlib.Path(source).open("r", encoding="utf-8") as file_handler:
                text = file_handler.read()
        elif isinstance(source, str):
            text = source
        elif isinstance(source, Iterable):
            global_counters = FrequencyAnalysis.get_counts()
            for path in source:
                counters = FrequencyAnalysis.get_counts(path)
                for c0, c1 in zip(global_counters, counters):
                    c0 += c1
            settings.logger.debug("Analysed {} source(s): {}".format(len(source), global_counters))
            return global_counters
        else:
            raise errors.IllegalParameter("Expect a Path or a str, received {} instead.".format(type(source)))
        # Analyze content:
        for line in text.split("\n"):
            line = Cleaner.clean(line).upper()
            for word in line.split(" "):
                m = len(word)
                for k, counter in enumerate(counters):
                    counter.update(word[i:i+k+1] for i in range(m-k))
        settings.logger.debug("Analysed a single source '{}': {}".format(str(source), counters))
        return counters

    @staticmethod
    def to_frequencies(counters):
        frequencies = []
        for counter in counters:
            df = pd.DataFrame.from_dict(dict(counter), orient="index", columns=["count"])
            df["frequency"] = df["count"]/df["count"].sum()
            df = df.sort_values("frequency", ascending=False)
            frequencies.append(df)
        return frequencies

    @staticmethod
    def analyze(source, n=3):
        counts = FrequencyAnalysis.get_counts(source, n=n)
        frequencies = FrequencyAnalysis.to_frequencies(counts)
        return frequencies


def main():
    paths = list((settings.resources/"books/fr/").glob("*.txt"))
    freqs = FrequencyAnalysis.analyze(paths)
    for f in freqs:
        print(f)


if __name__ == "__main__":
    main()
