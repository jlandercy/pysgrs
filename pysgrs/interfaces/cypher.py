import abc
import sys

from pysgrs.interfaces.alphabet import GenericAlphabet, Alphabet
from pysgrs.errors import BadParameter, IllegalIndexer


class GenericCypher(abc.ABC):

    def __init__(self, alphabet=None, key=None):

        if alphabet is None:
            self._alphabet = Alphabet()
        else:
            if isinstance(alphabet, GenericAlphabet):
                self._alphabet = alphabet
            else:
                raise BadParameter("Alphabet required, received {} instead".format(type(alphabet)))

        if key and not self.alphabet.contains(key):
            raise IllegalIndexer("Key '{}' cannot be expressed using {}".format(key, self.alphabet))
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
        if self.key is None:
            return 0
        else:
            return len(self.key)


class GenericStreamCypher(GenericCypher):

    def __init__(self, alphabet=None, key=None):
        super().__init__(alphabet=alphabet, key=key)

    def _apply(self, s, f, strict=False, quite=True):
        if not strict:
            s = s.upper()
        r = []
        for k, c in enumerate(s):
            try:
                x = f(c, k)
                r.append(x)
            except (AssertionError, ValueError) as err:
                if quite:
                    r.append(c)
                else:
                    raise IllegalIndexer("Character '{}' does not exist in {}: {}".format(c, self.alphabet, err))
        return "".join(r)

    def pairs(self, s=None):
        s = s or self.alphabet.alphabet
        return list(zip(s, self.cypher(s)))

    def to_networkx(self, s=None, raw=False):
        import networkx as nx
        g = nx.DiGraph()
        g.add_edges_from(self.pairs(s))
        if raw:
            return g
        else:
            import matplotlib.pyplot as plt
            fig, axe = plt.subplots()
            nx.draw_networkx(g)
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
