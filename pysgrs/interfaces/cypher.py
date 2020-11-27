import abc
import sys

from pysgrs.interfaces.alphabet import GenericAlphabet, Alphabet
from pysgrs.errors import BadParameter, IllegalCharacter


class GenericCypher(abc.ABC):

    def __init__(self, alphabet=None, key=None):

        if alphabet is None:
            self._alphabet = Alphabet()
        else:
            if isinstance(alphabet, GenericAlphabet):
                self._alphabet = alphabet
            else:
                raise BadParameter("Alphabet required, received {} instead".format(type(alphabet)))

        if key and not self.alphabet.isin(key):
            raise IllegalCharacter("Key '{}' cannot be expressed using {}".format(key, self.alphabet))
        else:
            self._key = key

    def __str__(self):
        return "<Cypher:{} alphabet={}>".format(self.__class__.__name__, self.alphabet)

    @abc.abstractmethod
    def _apply(self, s, f, strict=True, quite=False):
        pass

    @abc.abstractmethod
    def _cypher(self, c, k=None):
        pass

    @abc.abstractmethod
    def _decypher(self, c, k=None):
        pass

    def cypher(self, s, strict=True, quite=False):
        return self._apply(s, self._cypher, strict=strict, quite=quite)

    def decypher(self, s, strict=True, quite=False):
        return self._apply(s, self._decypher, strict=strict, quite=quite)

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def key(self):
        return self._key

    @property
    def keysize(self):
        return len(self._key)


class GenericStreamCypher(GenericCypher):

    def __init__(self, alphabet=None, key=None):
        super().__init__(alphabet=alphabet, key=key)

    def _apply(self, s, f, strict=True, quite=False):
        if not strict:
            s = s.upper()
        r = []
        for k, c in enumerate(s):
            try:
                if c != self.alphabet.joker:
                    x = self.alphabet.digit(f(c, k))
                else:
                    x = c
                r.append(x)
            except (AssertionError, ValueError) as err:
                if quite:
                    r.append(c)
                else:
                    raise IllegalCharacter("Character '{}' does not exist in {}: {}".format(c, self.alphabet, err))
        return "".join(r)

    @property
    def pairs(self):
        return list(zip(self.alphabet.alphabet, self.cypher(self.alphabet.alphabet)))

    @property
    def direct(self):
        return {x: y for (x, y) in self.pairs}

    @property
    def revere(self):
        return {y: x for (x, y) in self.pairs}

    @property
    def dataframe(self):
        import pandas as pd
        x = self.alphabet.dataframe
        y = pd.DataFrame(self.pairs, columns=["alphabet", "cypher"])
        y['cindices'] = y['cypher'].apply(lambda z: self.alphabet.alphabet.index(z))
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


# class FunctionalCypher(GenericStreamCypher):
#
#     def __init__(self, cypher, decypher=None, alphabet=None):
#         super().__init__(alphabet=alphabet)
#         self._cypher = cypher
#         self._decypher = decypher


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
