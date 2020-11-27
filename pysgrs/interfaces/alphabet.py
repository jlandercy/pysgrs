import sys
import itertools

from pysgrs import errors
#from pysgrs.settings import settings


class GenericAlphabet:
    """
    Provide commodities to handle Alphabet Map between Characters and Integers
    """

    def __init__(self, alphabet, indices=None, closure=None, joker='*'):

        self._joker = joker

        if indices is None:
            indices = list(range(len(alphabet)))

        if isinstance(alphabet, (list, tuple)):
            x = {}
            for (c, i) in alphabet:
                x[c] = i
            alphabet = x

        if isinstance(alphabet, dict):
            x = []
            y = []
            for k in sorted(alphabet):
                x.append(k)
                y.append(alphabet[k])
            alphabet = "".join(x)
            indices = y

        if closure is not None:
            alphabet += joker*len(closure)
            indices += closure

        self._alphabet = alphabet
        self._indices = indices

        assert isinstance(self.alphabet, str)
        assert all([isinstance(i, int) for i in self.indices])
        assert len(set(self.alphabet)) == len(self.alphabet) or closure is not None
        assert len(set(self.indices)) == len(self.indices)
        assert len(self.alphabet) == len(self.indices)

    def __str__(self):
        return "<Alphabet:{} (n={}) '{}'>".format(self.__class__.__name__, self.n, self.alphabet)

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def joker(self):
        return self._joker

    @property
    def n(self):
        return len(self.alphabet)

    def index(self, c):
        return self.indices[self.alphabet.index(c)]

    def digit(self, i):
        return self.alphabet[self.indices.index(i)]

    def encode(self, s):
        return [self.index(c) for c in s]

    def decode(self, l, sep=""):
        return sep.join([self.digit(i) for i in l])

    @property
    def indices(self):
        return self._indices

    @property
    def pairs(self):
        return list(zip(self.alphabet, self.indices))

    @property
    def direct(self):
        return {c: i for (c, i) in self.pairs}

    @property
    def inverse(self):
        return {i: c for (c, i) in self.pairs}

    @property
    def dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.pairs, columns=['alphabet', 'indices'])

    def product(self, n):
        for x in itertools.product(self.alphabet, repeat=n):
            yield "".join(x)

    def replacements(self, n):
        for x in itertools.combinations_with_replacement(self.alphabet, n):
            yield "".join(x)

    def combinations(self, n):
        for x in itertools.combinations(self.alphabet, n):
            yield "".join(x)

    def permutations(self, n):
        for x in itertools.permutations(self.alphabet, n):
            yield "".join(x)


class Alphabet(GenericAlphabet):

    _offset = 65

    def __init__(self):
        super().__init__("".join([chr(x + Alphabet._offset) for x in range(26)]))

    def index(self, c, quite=False):
        if not quite:
            assert 0 <= ord(c) - Alphabet._offset < 26
        return ord(c) - Alphabet._offset

    def digit(self, i):
        return chr(i + Alphabet._offset)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
