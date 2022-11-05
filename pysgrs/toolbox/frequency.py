import abc
import collections
from collections.abc import Iterable
import pathlib

import numpy as np
import pandas as pd

from pysgrs.settings import settings
from pysgrs import errors
from pysgrs.toolbox.shapers import Shaper
from pysgrs.toolbox.cleaner import AsciiCleaner


class Analyzer(abc.ABC):

    @abc.abstractmethod
    def analyze(self, source):
        pass


class FrequencyAnalyzer(Analyzer):

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
            line = AsciiCleaner.clean(line).upper()
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
    def keysize_coincidences(text, min_key_size=1, max_key_size=25):
        code_size = len(text)
        coincidences = []
        for ncol in np.arange(min_key_size, max_key_size + 1):
            nrow = int(np.ceil(code_size / ncol))
            block = Shaper.to_matrix(text, shape=(nrow, ncol))
            for k in np.arange(ncol):
                column = Shaper.to_str(block[:, k])
                coincidence = FrequencyAnalyzer.analyze(column, max_ngram=1)[0].sum()["coincidence"]
                coincidences.append({"key_size": ncol, "column_index": k, "coincidence": coincidence})
        return pd.DataFrame(coincidences)
