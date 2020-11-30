import sys
import itertools

from pysgrs import errors


class GenericAlphabet:
    pass


class GenericMixedAlphabet(GenericAlphabet):
    """
    Generic SimpleAlphabet:
    Mapping between symbols (as a string) and indices (as a sequence of integers or strings).
    If no indices are provided range(size) is used.
    Mapping can be provided in several fashions (strings, list, dict)
    """

    _allowed_types = (int, str)

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

        if not isinstance(symbols, str):
            raise errors.IllegalAlphabetParameter(
                "Symbols must be of type str, received {} instead".format(type(symbols)))

        if not all([isinstance(i, self._allowed_types) for i in indices]):
            raise errors.IllegalAlphabetParameter(
                "Indices must be of type {}, received {} instead".format(self._allowed_types, self.index_types))

        if not len(set(symbols)) == len(symbols):
            raise errors.IllegalAlphabetParameter("Symbols must be unique")

        if not len(set(indices)) == len(indices):
            raise errors.IllegalAlphabetParameter("Indices must be unique")

        if not len(symbols) == len(indices):
            raise errors.IllegalAlphabetParameter("Symbols and Indices must have the same number of elements")

        self._symbols = symbols
        self._indices = tuple(indices)

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
    def index_types(self):
        return set([type(x) for x in self.indices])

    @property
    def is_index_mixed_types(self):
        return len(self.index_types) > 1

    @property
    def is_natural(self):
        return self.indices == tuple(range(self.size))

    @property
    def is_strictly_increasing(self):
        if self.is_index_mixed_types:
            raise errors.IllegalAlphabetOperation("Mixed types index cannot be compared")
        else:
            return all(x < y for x, y in zip(self.indices, self.indices[1:]))

    @property
    def is_strictly_decreasing(self):
        if self.is_index_mixed_types:
            raise errors.IllegalAlphabetOperation("Mixed types index cannot be compared")
        else:
            return all(x > y for x, y in zip(self.indices, self.indices[1:]))

    @property
    def is_monotonic(self):
        return self.is_strictly_increasing or self.is_strictly_decreasing

    @property
    def size(self):
        return len(self.symbols)

    def index(self, c):
        try:
            return self.indices[self.symbols.index(c)]
        except ValueError:
            raise errors.IllegalAlphabetIndex("Cannot index with <{}> for {}".format(c, self))

    def symbol(self, k):
        try:
            return self.symbols[self.indices.index(k)]
        except ValueError:
            raise errors.IllegalAlphabetIndex("Cannot index with <{}> for {}".format(k, self))

    def contains(self, s):
        return all([(c in self.symbols) for c in s])

    def __getitem__(self, item):
        if (isinstance(item, str) and item in self.symbols) and item in self.indices:
            raise errors.AmbiguousAlphabetIndex("Key <{}> is present in both symbols and indices".format(item))
        elif isinstance(item, str) and item in self.symbols:
            return self.index(item)
        elif item in self.indices:
            return self.symbol(item)
        else:
            raise errors.IllegalAlphabetIndex("Key <{}> is not present in both symbols and indices".format(item))

    def __setitem__(self, key, value):
        raise errors.IllegalAlphabetOperation("Assignation is not allowed for Alphabet")

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


class GenericIntegerAlphabet(GenericMixedAlphabet):

    _allowed_types = (int,)


class GenericStringAlphabet(GenericMixedAlphabet):

    _allowed_types = (str,)

    @property
    def index_symbols(self):
        return set("".join(self.indices))

    @property
    def index_symbol_size(self):
        return len(self.index_symbols)

    @property
    def index_sizes(self):
        return [len(x) for x in self.indices]

    @property
    def index_min_size(self):
        return min(self.index_sizes)

    @property
    def index_max_size(self):
        return max(self.index_sizes)

    @property
    def is_index_size_constant(self):
        return self.index_min_size == self.index_max_size


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
