import sys

from pysgrs import errors
#from pysgrs.settings import settings


class GenericAlphabet:
    """
    Provide commodities to handle Alphabet Map between Characters and Integers
    """

    def __init__(self, alphabet, indices=None):

        if indices is None:
            self._indices = list(range(len(alphabet)))
        else:
            self._indices = indices

        if isinstance(alphabet, str):
            self._alphabet = alphabet

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
            self._alphabet = "".join(x)
            self._indices = y

        assert isinstance(self.alphabet, str)
        assert all([isinstance(i, int) for i in self.indices])
        assert len(set(self.alphabet)) == len(self.alphabet)
        assert len(set(self.indices)) == len(self.indices)
        assert len(self.alphabet) == len(self.indices)

    def __str__(self):
        return "<Alphabet({}) '{}'>".format(self.n, self.alphabet)

    @property
    def alphabet(self):
        return self._alphabet

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


class Alphabet(GenericAlphabet):

    _offset = 65

    def __init__(self):
        super().__init__("".join([chr(x + Alphabet._offset) for x in range(26)]))

    def index(self, c):
        assert 0 <= ord(c) - Alphabet._offset < 26
        return ord(c) - Alphabet._offset

    def digit(self, i):
        return chr(i + Alphabet._offset)


class Cypher:

    def __init__(self, alphabet=None, offset=0):

        self._offset = offset
        if alphabet is None:
            self._alphabet = Alphabet()

    @property
    def offset(self):
        return self._offset

    @property
    def alphabet(self):
        return self._alphabet

    def _cypher(self, x):
        return (x + self.offset) % self.alphabet.n

    def _decypher(self, x):
        return (x - self.offset) % self.alphabet.n

    def _apply(self, s, func, strict=True, quite=False):
        if not strict:
            s = s.upper()
        r = []
        for c in s:
            try:
                x = self.alphabet.digit(func(self.alphabet.index(c)))
                r.append(x)
            except (AssertionError, ValueError) as err:
                if quite:
                    r.append(c)
                else:
                    raise errors.IllegalCharacter("Character '{}' does not exist in {}".format(c, self.alphabet))
        return "".join(r)

    def cypher(self, s, strict=True, quite=False):
        return self._apply(s, self._cypher, strict=strict, quite=quite)

    def decypher(self, s, strict=True, quite=False):
        return self._apply(s, self._decypher, strict=strict, quite=quite)

    @property
    def pairs(self):
        return list(zip(self.alphabet.alphabet, self.cypher(self.alphabet.alphabet)))

    @property
    def direct(self):
        return {x: y for (x, y) in self.pairs}

    @property
    def dataframe(self):
        import pandas as pd
        x = self.alphabet.dataframe
        y = pd.DataFrame(self.pairs, columns=["alphabet", "cypher"])
        y['cindices'] = y['cypher'].apply(lambda x: self.alphabet.alphabet.index(x))
        return x.merge(y, on="alphabet")

    def graph(self, seed=10, pos=None):
        import matplotlib.pyplot as plt
        import networkx as nx
        G = nx.DiGraph()
        G.add_edges_from(self.pairs)
        if pos is True:
            pos = nx.spring_layout(G, seed=seed)
        fig, axe = plt.subplots()
        nx.draw_networkx(G, pos=pos, arrows=True, ax=axe)
        plt.show()
        return axe


def main():

    C = Cypher(offset=3)
    print(C.cypher("CAVECANEM", quite=False))
    print(C.decypher("FDYH fDQHP", strict=False, quite=True))

    sys.exit(0)


if __name__ == "__main__":
    main()
