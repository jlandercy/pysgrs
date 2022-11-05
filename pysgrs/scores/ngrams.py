import sys
import collections
import pathlib
import json

import numpy as np

from pysgrs.interfaces.score import GenericScore
from pysgrs.settings import settings
from pysgrs import errors
from pysgrs.toolbox.cleaner import AsciiCleaner


class NGramScore(GenericScore):

    def __init__(self, source=None, order=1, language="fr", floor=0.01, scaler=np.log10):

        self._language = language

        if source is None:
            source = settings.resources / 'ngrams/ngrams_{}.json'.format(self.language)

        if isinstance(source, (str, pathlib.Path)):
            source = pathlib.Path(source)
            with source.open() as fh:
                source = json.load(fh)
            values = source["%d-grams" % order]
            source = {k: v for k, v in zip(values["ngram"], values["count"])}

        if isinstance(source, collections.Counter):
            source = dict(source)

        if not isinstance(source, dict):
            raise errors.IllegalParameter("Requires a dict or a path, received {} instead".format(type(source)))

        if not all(isinstance(c, str) for c in source.keys()):
            raise errors.IllegalParameter("All keys must be string, received instead")

        if not all(isinstance(c, int) and (c > 0) for c in source.values()):
            raise errors.IllegalParameter("All values must be positive integer, received instead")

        self._order = len(tuple(source.keys())[0])

        if not all(len(ngram) == self.order for ngram in source):
            raise errors.IllegalParameter("All keys must have the same length")

        self._counts = source
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
        return "<NGramScore language='{}' order={} size={} floor={:.3f} scaler={}>".format(
            self.language, self.order, self.size, self.floor, self.scaler.__name__)

    def __repr__(self):
        return self.__str__()

    @property
    def language(self):
        return self._language

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
        settings.logger.debug("Score: {:.3f} for '{}' with {}".format(score, text[:16], self))
        return score


class MultiNGramScore(GenericScore):

    def __init__(self, source=None, language="fr", min_order=1, max_order=5):

        if source is None:
            source = settings.resources / 'ngrams/ngrams_{}.json'.format(language)

        if isinstance(source, (str, pathlib.Path)):
            source = pathlib.Path(source)
            with source.open() as fh:
                source = json.load(fh)

        self._ngrams = dict()
        for order in range(min_order, max_order+1):
            ngram = NGramScore(order=order, language=language)
            self._ngrams[ngram.order] = ngram

    def __str__(self):
        return "<MultiNGramScore ngrams={}>".format(self.ngrams)

    @property
    def ngrams(self):
        return self._ngrams

    def score(self, text):
        return {"score-%d" % ngram.order: ngram.score(text) for ngram in self.ngrams.values()}


class MixedNGramScore(GenericScore):

    def __init__(self, source=None, language="fr", weights=(0.6, 0.3, 0.1)):
        self.sub_scores = MultiNGramScore(source=source, language=language, min_order=1, max_order=len(weights))
        if not np.sum(weights) == 1:
            raise ValueError("Sum of weights must be equal to unity")
        self.score_weights = np.array(weights)

    @property
    def orders(self):
        return np.arange(len(self.score_weights)) + 1

    def score(self, text):
        return np.sum(np.array([self.sub_scores.ngrams[order].score(text) for order in self.orders])*self.score_weights)


def main():

    x = MultiNGramScore()
    #x = NGramScore()
    print(x)

    sys.exit(0)


if __name__ == "__main__":
    main()
