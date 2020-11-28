import abc
import sys

from pysgrs.interfaces.alphabet import GenericAlphabet, Alphabet
from pysgrs.errors import BadParameter, IllegalIndexer
from pysgrs.settings import settings


class GenericCypher(abc.ABC):

    def __init__(self, alphabet=None, key=None):

        if alphabet is None:
            self._alphabet = Alphabet()
        else:
            if isinstance(alphabet, GenericAlphabet):
                self._alphabet = alphabet
            else:
                raise BadParameter("Alphabet is required, received {} instead".format(type(alphabet)))

        if key and not(key in self.alphabet):
            raise IllegalIndexer("Key '{}' cannot be expressed with {}".format(key, self.alphabet))
        else:
            self._key = key

    def __str__(self):
        return "<Cypher:{} symbols={}>".format(self.__class__.__name__, self.alphabet)

    @abc.abstractmethod
    def _apply(self, s, f, strict=True, quite=False):
        pass

    @abc.abstractmethod
    def _cypher(self, c, k=None):
        pass

    @abc.abstractmethod
    def _decypher(self, c, k=None):
        pass

    def cypher(self, s, strict=False, quite=True):
        return self._apply(s, self._cypher, strict=strict, quite=quite)

    def decypher(self, s, strict=False, quite=True):
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
        q = 0
        r = []
        for k, c in enumerate(s):
            try:
                if strict:
                    x = f(c, k - q)
                else:
                    x = f(c.upper(), k - q)
                    if c.islower():
                        x = x.lower()
                r.append(x)
            except IllegalIndexer as err:
                if quite:
                    q += 1
                    r.append(c)
                else:
                    raise err
        r = "".join(r)
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, f.__name__, s, r))
        return r

    def pairs(self, s=None):
        s = s or self.alphabet.symbols
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
#     def __init__(self, cypher, decypher=None, symbols=None):
#         super().__init__(symbols=symbols)
#         self._cypher = cypher
#         self._decypher = decypher


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
