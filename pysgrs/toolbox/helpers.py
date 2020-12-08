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
from pysgrs.toolbox.formats import Shaper


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


class FrequencyAnalyzer:

    @staticmethod
    def get_counts(source=None, max_ngram=3):
        counters = [collections.Counter() for i in range(max_ngram)]
        # Parse arguments:
        if source is None:
            return counters
        if isinstance(source, pathlib.Path):
            with pathlib.Path(source).open("r", encoding="utf-8") as file_handler:
                text = file_handler.read()
        elif isinstance(source, str):
            text = source
        elif isinstance(source, Iterable):
            global_counters = FrequencyAnalyzer.get_counts(max_ngram=max_ngram)
            for path in source:
                counters = FrequencyAnalyzer.get_counts(path, max_ngram=max_ngram)
                for c0, c1 in zip(global_counters, counters):
                    c0 += c1
            settings.logger.debug("Analysed {} source(s): {} counter(s)".format(len(source), len(global_counters)))
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
        settings.logger.debug("Analysed source '{}': {} counter(s)".format(str(source), len(counters)))
        return counters

    @staticmethod
    def to_frequencies(counters):
        frequencies = []
        for counter in counters:
            df = pd.DataFrame.from_dict(dict(counter), orient="index", columns=["count"])
            df.index.name = "ngram"
            n = df["count"].sum()
            df["frequency"] = df["count"]/n
            df["log_frequency"] = np.log(df["frequency"])
            df["log10_frequency"] = np.log10(df["frequency"])
            df["coincidence"] = df.shape[0]*df["count"]*(df["count"] - 1)/(n*(n-1))
            df = df.sort_values("frequency", ascending=False).reset_index()
            df["order"] = df["ngram"].apply(len)
            frequencies.append(df)
        return frequencies

    @staticmethod
    def analyze(source=None, max_ngram=3, language="fr"):
        if source is None:
            source = list((settings.resources / "books/{}/".format(language)).glob("*.txt"))
        counts = FrequencyAnalyzer.get_counts(source, max_ngram=max_ngram)
        frequencies = FrequencyAnalyzer.to_frequencies(counts)
        return frequencies

    @staticmethod
    def to_format(source=None, max_ngram=3, language="fr"):
        frequencies = FrequencyAnalyzer.analyze(source=source, max_ngram=max_ngram, language=language)
        ngrams = dict()
        for i, frequency in enumerate(frequencies):
            ngrams["%d-grams" % (i+1)] = frequency[["ngram", "count"]].to_dict(orient="list")
        return ngrams

    @staticmethod
    def keysize_coincidences(s, max_keysize=25):
        code_size = len(s)
        coincidences = []
        for ncol in np.arange(1, max_keysize + 1):
            nrow = int(np.ceil(code_size / ncol))
            block = Shaper.to_matrix(s, shape=(nrow, ncol))
            for k in np.arange(ncol):
                column = Shaper.to_str(block[:, k])
                coincidence = FrequencyAnalyzer.analyze(column, max_ngram=1)[0].sum()["coincidence"]
                coincidences.append({"keysize": ncol, "column": k, "coincidence": coincidence})
        return pd.DataFrame(coincidences)


class NGram:

    def __init__(self, ngrams, floor=0.01, scaler=np.log10):

        if isinstance(ngrams, collections.Counter):
            ngrams = dict(ngrams)

        if not isinstance(ngrams, dict):
            raise errors.IllegalParameter("Requires a dict or a path, received {} instead".format(type(ngrams)))

        if not all(isinstance(c, str) for c in ngrams.keys()):
            raise errors.IllegalParameter("All keys must be string, received instead")

        if not all(isinstance(c, int) and (c > 0) for c in ngrams.values()):
            raise errors.IllegalParameter("All values must be positive integer, received instead")

        self._order = len(tuple(ngrams.keys())[0])

        if not all(len(ngram) == self.order for ngram in ngrams):
            raise errors.IllegalParameter("All keys must have the same length")

        self._counts = ngrams
        self._total = sum(self.counts.values())

        self._scaler = scaler
        self._floor = self.scaler(floor/self.total)
        self._frequency = {k: float(v) / self.total for k, v in self.counts.items()}

        if not np.isclose(np.sum(tuple(self.frequency.values())), 1.):
            raise errors.IllegalParameter("Probability sum must converge to unit")

        self._likelihood = {k: self.scaler(v) for k, v in self.frequency.items()}

        if not all(x > self.floor for x in self.likelihood.values()):
            raise errors.IllegalParameter("Floor must be lower than all existing likelihood")

    def __str__(self):
        return "<NGram order={} size={} floor={} scaler={}>".format(self.order, self.size, self.floor, self.scaler)

    @property
    def order(self):
        return self._order

    @property
    def floor(self):
        return self._floor

    @property
    def scaler(self):
        return self._scaler

    @property
    def counts(self):
        return self._counts

    @property
    def total(self):
        return self._total

    @property
    def frequency(self):
        return self._frequency

    @property
    def likelihood(self):
        return self._likelihood

    @property
    def size(self):
        return len(self.counts)

    def __len__(self):
        return self.size

    def contains(self, item):
        return item in self.counts

    def __contains__(self, item):
        return self.contains(item)

    def score(self, text):
        n = len(text)
        score = 0.
        for k in range(n - self.size + 1):
            ngram = text[k:(k+self.size)]
            score += self.likelihood.get(ngram, self.floor)
        return score


def main():
    import json


    p = pathlib.Path(__file__).parent / 'resources/ngrams_fr.json'

    with p.open() as fh:
        data = json.load(fh)

    for k, (key, values) in enumerate(data.items()):
        d = {k: v for k, v in zip(values["ngram"], values["count"])}
        N = NGram(d)
        print(N)

    # freqs = FrequencyAnalyzer.to_format(max_ngram=5)
    # with p.open("w") as fh:
    #     json.dump(freqs, fh)

    # freqs = FrequencyAnalyzer.analyze()
    # for f in freqs:
    #     print(f.iloc[:500,:].reset_index().to_json(orient="records"))
    #     print(f)
    #     print(f.sum())

    sys.exit(0)


if __name__ == "__main__":
    main()
