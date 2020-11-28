import sys
import itertools

from pysgrs.errors import IllegalOperation, IllegalIndexer, IllegalIndexerType, IllegalIndex, IllegalSymbol


class GenericAlphabet:
    """
    Generic Alphabet:
    Mapping between symbols (characters) and indices (integers).
    If no indices are provided range(size) is used.
    Mapping can be provided in several fashion (list, dict)
    """

    def __init__(self, symbols, indices=None):

        if indices is None:
            indices = list(range(len(symbols)))

        if isinstance(symbols, (list, tuple)):
            x = {}
            for (c, i) in symbols:
                x[c] = i
            symbols = x

        if isinstance(symbols, dict):
            x = []
            y = []
            for k in sorted(symbols):
                x.append(k)
                y.append(symbols[k])
            symbols = "".join(x)
            indices = y

        self._symbols = symbols
        self._indices = tuple(indices)

        assert isinstance(self.symbols, str)
        assert all([isinstance(i, int) for i in self.indices])
        assert len(set(self.symbols)) == len(self.symbols)
        assert len(set(self.indices)) == len(self.indices)
        assert len(self.symbols) == len(self.indices)

    def __str__(self):
        if self.is_natural:
            return "<{} size={} symbols='{}'>".format(self.__class__.__name__, self.size, self.symbols)
        else:
            return "<{} size={} symbols='{}' indices={}>".format(self.__class__.__name__, self.size,
                                                                 self.symbols, self.indices)

    @property
    def symbols(self):
        return self._symbols

    @property
    def indices(self):
        return self._indices

    @property
    def is_natural(self):
        return self.indices == tuple(range(self.size))

    @property
    def size(self):
        return len(self.symbols)

    def index(self, c):
        try:
            return self.indices[self.symbols.index(c)]
        except ValueError:
            raise IllegalSymbol("Cannot index with '{}' for {}".format(c, self))

    def symbol(self, k):
        try:
            return self.symbols[self.indices.index(k)]
        except ValueError:
            raise IllegalIndex("Cannot index with {} for {}".format(k, self))

    def contains(self, s):
        return all([(c in self.symbols) for c in s])

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.index(item)
        elif isinstance(item, int):
            return self.symbol(item)
        else:
            raise IllegalIndexerType("Bad Alphabet indexer type (str or int), received {} instead".format(type(item)))

    def __setitem__(self, key, value):
        raise IllegalOperation("Assignation is not allowed for Alphabet")

    def __contains__(self, item):
        return self.contains(item)

    def encode(self, s):
        return [self.index(c) for c in s]

    def decode(self, s, sep=""):
        return sep.join([self.symbol(i) for i in s])

    def pairs(self):
        return list(zip(self.symbols, self.indices))

    def direct(self):
        return {c: i for (c, i) in self.pairs()}

    def inverse(self):
        return {i: c for (c, i) in self.pairs()}

    def to_dataframe(self):
        import pandas as pd
        return pd.DataFrame(self.pairs(), columns=['symbol', 'index'])

    def product(self, n):
        for x in itertools.product(self.symbols, repeat=n):
            yield "".join(x)

    def replacements(self, n):
        for x in itertools.combinations_with_replacement(self.symbols, n):
            yield "".join(x)

    def combinations(self, n):
        for x in itertools.combinations(self.symbols, n):
            yield "".join(x)

    def permutations(self, n):
        for x in itertools.permutations(self.symbols, n):
            yield "".join(x)


class Alphabet(GenericAlphabet):
    """
    Base Alphabet [A-Z]:
    Using commodities from Generic Alphabet but replacing indexing by ASCII index manipulation for efficiency sake.
    """

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
            raise IllegalSymbol("Symbol '{}' outside allowed range of {}".format(c, self))

    def symbol(self, k):
        if 0 <= k < self.size:
            return chr(k + self.offset)
        else:
            raise IllegalIndex("Index {} outside allowed range of {}".format(k, self))


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
