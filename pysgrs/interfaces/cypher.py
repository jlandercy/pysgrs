import sys
import itertools

from pysgrs.interfaces.alphabet import Alphabet
from pysgrs.errors import IllegalCharacter


class GenericCypher:

    def __init__(self, alphabet=None):

        if alphabet is None:
            self._alphabet = Alphabet()
        else:
            self._alphabet = alphabet

    def __str__(self):
        return "<Cypher:{} alphabet={}>".format(self.__class__.__name__, self.alphabet)

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
                if c != self.alphabet.joker:
                    x = self.alphabet.digit(func(self.alphabet.index(c)))
                else:
                    x = c
                r.append(x)
            except (AssertionError, ValueError) as err:
                if quite:
                    r.append(c)
                else:
                    #raise err
                    raise IllegalCharacter("Character '{}' does not exist in {}".format(c, self.alphabet))
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





class FunctionalCypher(GenericCypher):

    def __init__(self, cypher, decypher=None, alphabet=None):
        super().__init__(alphabet=alphabet)
        self._cypher = cypher
        self._decypher = decypher


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
