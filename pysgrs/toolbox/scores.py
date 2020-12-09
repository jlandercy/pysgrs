import abc
import sys
import collections
import pathlib
import json

import numpy as np

from pysgrs.settings import settings
from pysgrs import errors
from pysgrs.toolbox.cleaner import AsciiCleaner


class GenericScore(abc.ABC):

    @abc.abstractmethod
    def score(self, text, **kwargs):
        pass


class NGramScore(GenericScore):

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
        return "<NGramScore order={} size={} floor={:.3f} scaler={}>".format(
            self.order, self.size, self.floor, self.scaler.__name__)

    def __repr__(self):
        return self.__str__()

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

    def score(self, text, normalize=True):
        if normalize:
            text = AsciiCleaner.normalize(text)
        n = len(text)
        score = 0.
        for k in range(n - self.order + 1):
            ngram = text[k:(k+self.order)]
            score += self.likelihood.get(ngram, self.floor)
        return score


class MultiNGramScore(GenericScore):

    def __init__(self, source=None, language="fr"):

        if source is None:
            source = pathlib.Path(__file__).parent / 'resources/ngrams_{}.json'.format(language)

        if isinstance(source, (str, pathlib.Path)):
            source = pathlib.Path(source)
            with source.open() as fh:
                source = json.load(fh)

        self._ngrams = dict()
        for key, values in source.items():
            d = {k: v for k, v in zip(values["ngram"], values["count"])}
            ngram = NGramScore(d)
            self._ngrams[ngram.order] = ngram

    def __str__(self):
        return "<MultiNGramScore ngrams={}>".format(self.ngrams)

    @property
    def ngrams(self):
        return self._ngrams

    def score(self, text):
        return {"score-%d" % ngram.order: ngram.score(text) for ngram in self.ngrams.values()}


def main():

    x = MultiNGramScore()
    print(x)

    sys.exit(0)


if __name__ == "__main__":
    main()
