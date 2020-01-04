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


class GenericCypher:

    def __init__(self, alphabet=None):

        if alphabet is None:
            self._alphabet = Alphabet()
        else:
            self._alphabet = alphabet

    def __str__(self):
        return "<Cypher alphabet={}>".format(self.alphabet)

    @property
    def alphabet(self):
        return self._alphabet

    def _cypher(self, x):
        raise NotImplemented

    def _decypher(self, x):
        raise NotImplemented

    def _apply(self, s, func, strict=True, quite=False):
        if not strict:
            s = s.upper()
        r = []
        for c in s:
            try:
                if c != self.alphabet._joker:
                    x = self.alphabet.digit(func(self.alphabet.index(c)))
                else:
                    x = c
                r.append(x)
            except (AssertionError, ValueError) as err:
                if quite:
                    r.append(c)
                else:
                    raise err
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

    @property
    def graph(self):
        import networkx as nx
        G = nx.DiGraph()
        G.add_nodes_from(list(self.alphabet.alphabet))
        G.add_edges_from(self.pairs)
        return G

    def plot(self, pos=None, **kwargs):
        import matplotlib.pyplot as plt
        import networkx as nx
        G = self.graph
        if pos is None:
            pos = nx.circular_layout(G)
        fig, axe = plt.subplots()
        nx.draw_networkx(G, pos=pos, arrows=True, ax=axe, **kwargs)
        return axe


class Caesar(GenericCypher):

    def __init__(self, alphabet=None, offset=0):
        super().__init__(alphabet=alphabet)
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    def _cypher(self, x):
        return (x + self.offset) % self.alphabet.n

    def _decypher(self, x):
        return (x - self.offset) % self.alphabet.n


class FunctionalCypher(GenericCypher):

    def __init__(self, cypher, decypher=None, alphabet=None):
        super().__init__(alphabet=alphabet)
        self._cypher = cypher
        if decypher is not None:
            self._decypher = decypher


def main():

    import matplotlib.pyplot as plt
    import networkx as nx

    def polynom(x):
        return (-3*(x-2)**4 - 6*(x-9)**2 + 7*(x-9)**6) % 23

    A = GenericAlphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ", list(range(1, 27)), closure=[0,-1])
    print(A)
    print(A.alphabet)
    print(A.indices)
    C = FunctionalCypher(cypher=polynom, alphabet=A)
    G = C.graph
    pos = nx.spring_layout(G, seed=10, scale=10)
    C.plot(pos=pos)
    plt.show()

    sys.exit(0)


if __name__ == "__main__":
    main()
