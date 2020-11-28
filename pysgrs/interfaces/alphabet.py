import sys
import itertools

from pysgrs.errors import IllegalOperation, IllegalIndexer


class GenericAlphabet:
    """
    Provide commodities to handle Alphabet Map between Characters and Integers
    """

    def __init__(self, alphabet, indices=None):

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

        self._alphabet = alphabet
        self._indices = indices

        assert isinstance(self.alphabet, str)
        assert all([isinstance(i, int) for i in self.indices])
        assert len(set(self.alphabet)) == len(self.alphabet)
        assert len(set(self.indices)) == len(self.indices)
        assert len(self.alphabet) == len(self.indices)

    def __str__(self):
        return "<Alphabet:{} '{}' (size={})>".format(self.__class__.__name__, self.alphabet, self.size)

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def indices(self):
        return self._indices

    @property
    def size(self):
        return len(self.alphabet)

    def index(self, c):
        try:
            return self.indices[self.alphabet.index(c)]
        except ValueError:
            raise IllegalIndexer("Cannot index with '{}' for {}".format(c, self))

    def digit(self, k):
        try:
            return self.alphabet[self.indices.index(k)]
        except ValueError:
            raise IllegalIndexer("Cannot index with {} for {}".format(k, self))

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.alphabet.index(item)
        elif isinstance(item, int):
            return self.alphabet.digit(item)
        else:
            raise IllegalIndexer("Bad Alphabet indexer type (str or int), received {} instead".format(type(item)))

    def __setitem__(self, key, value):
        raise IllegalOperation("Assignation is invalid for Alphabet")

    def encode(self, s):
        return [self.index(c) for c in s]

    def decode(self, s, sep=""):
        return sep.join([self.digit(i) for i in s])

    def contains(self, s):
        return all([(c in self.alphabet) for c in s])

    def __contains__(self, item):
        return self.contains(item)

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
        return pd.DataFrame(self.pairs, columns=['digit', 'index'])

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

    def __init__(self, offset=65, size=26):
        super().__init__("".join([chr(x + offset) for x in range(size)]))
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    def index(self, c):
        if 0 <= ord(c) - self.offset < self.size:
            return ord(c) - self.offset
        else:
            raise IllegalIndexer("Index {} outside allowed range of {}".format(c, self))

    def digit(self, k):
        if 0 <= k < self.size:
            return chr(k + self.offset)
        else:
            raise IllegalIndexer("Index {} outside allowed range of {}".format(k, self))


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
