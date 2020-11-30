import abc
import sys

import numpy as np
import pandas as pd

#import unidecode
#import unicodedata

from pysgrs import alphabets
from pysgrs import errors
from pysgrs.settings import settings


class GenericCypher(abc.ABC):

    def __str__(self):
        return "<{}>".format(self.__class__.__name__)

    @abc.abstractmethod
    def cypher(self, s, **kwargs):
        pass

    @abc.abstractmethod
    def decypher(self, s, **kwargs):
        pass


class GenericAlphabetCypher(GenericCypher):

    def __init__(self, alphabet=None, key=None):

        if alphabet is None:
            self._alphabet = alphabets.SimpleAlphabet()
        else:
            if isinstance(alphabet, alphabets.GenericAlphabet):
                self._alphabet = alphabet
            else:
                raise errors.IllegalParameter("Alphabet is required, received {} instead".format(type(alphabet)))

        if key and not(key in self.alphabet):
            raise errors.IllegalAlphabetIndex("Key '{}' cannot be expressed with {}".format(key, self.alphabet))
        else:
            self._key = key

    def __str__(self):
        if self.keysize > 0:
            return "<{} keysize={} alphabet={}>".format(self.__class__.__name__, self.keysize, self.alphabet)
        else:
            return "<{} alphabet={}>".format(self.__class__.__name__, self.alphabet)

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


class GenericAlphabetStreamCypher(GenericAlphabetCypher):

    def __init__(self, alphabet=None, key=None):
        super().__init__(alphabet=alphabet, key=key)
        if not isinstance(self.alphabet, alphabets.GenericIntegerAlphabet):
            raise errors.IllegalCypherParameter("Generic Stream Cypher requires Integer Alphabet.")

    def _apply(self, s, f, strict=False, quite=True):
        q = 0
        r = []
        for k, c in enumerate(s):
            try:
                if strict:
                    x = f(c, k - q)
                else:
                    #c = unicodedata.normalize('NFD', c).encode("ascii", "ignore").decode("utf-8")
                    #c = unidecode.unidecode(c)
                    x = f(c.upper(), k - q)
                    if c.islower():
                        x = x.lower()
                r.append(x)
            except errors.IllegalAlphabetIndex as err:
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
        c = self.cypher(s)
        return list(zip(s, c))

    def to_dataframe(self, s=None):
        return pd.DataFrame(self.pairs(s), columns=["clear", "cypher"])

    def to_graph(self, s=None, raw=False):
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


class GenericNaturalAlphabetStreamCypher(GenericAlphabetStreamCypher):

    def __init__(self, alphabet=None, key=None):
        super().__init__(alphabet=alphabet, key=key)
        if not self.alphabet.is_natural:
            raise errors.IllegalCypherParameter("Generic Stream Cypher requires Natural Alphabet.")


class GenericShapeCypher(GenericCypher):

    def __init__(self, shape=None, pad=" "):
        self._shape = shape
        self._pad = pad

    def __str__(self):
        return "<{} shape={} pad='{}'>".format(self.__class__.__name__, self.shape, self.pad)

    @property
    def shape(self):
        return self._shape

    @property
    def pad(self):
        return self._pad

    def get_shapes(self, s, shape=None):
        n = len(s)
        m = np.sqrt(n)
        mmin = int(np.floor(m))
        mmax = int(np.ceil(m))
        shapes = [
            {"id": "lowsquare", "shape": (mmin, mmin)},
            {"id": "lowrect", "shape": (mmin, mmax)},
            {"id": "uprect", "shape": (mmax, mmin)},
            {"id": "upsquare", "shape": (mmax, mmax)},
        ]
        if shape:
            shapes.append({"id": "user", "shape": shape})
        if self.shape:
            shapes.append({"id": "default", "shape": self.shape})
        df = pd.DataFrame(shapes)
        df["size"] = df["shape"].apply(np.prod)
        df["padding"] = df["size"] - n
        df["valid"] = df["padding"] >= 0
        df = df.set_index("id")
        mopt = df.loc[df["valid"], "padding"].min()
        df.loc["auto", :] = df.loc[df["padding"] == mopt, :].iloc[0, :]
        return df


class GenericCodexCypher(GenericCypher):
    pass


class GenericBaseCypher(GenericCypher):
    pass


# class FunctionalCypher(GenericAlphabetCypher):
#
#     def __init__(self, cypher, decypher=None, symbols=None):
#         super().__init__(symbols=symbols)
#         self._cypher = cypher
#         self._decypher = decypher


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
