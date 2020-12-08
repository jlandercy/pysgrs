import abc
import sys

import numpy as np
import pandas as pd

from pysgrs import alphabets
from pysgrs import errors
from pysgrs import toolbox
from pysgrs.settings import settings


class GenericCipher(abc.ABC):

    def __str__(self):
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()

    @abc.abstractmethod
    def encipher(self, s, **kwargs):
        pass

    @abc.abstractmethod
    def decipher(self, s, **kwargs):
        pass


class GenericFunctionalCipher(GenericCipher):

    @abc.abstractmethod
    def _apply(self, s, f, strict=True, quite=False):
        pass

    @abc.abstractmethod
    def _encipher(self, c, k=None):
        pass

    @abc.abstractmethod
    def _decipher(self, c, k=None):
        pass

    def encipher(self, s, strict=False, quite=True):
        return self._apply(s, self._encipher, strict=strict, quite=quite)

    def decipher(self, s, strict=False, quite=True):
        return self._apply(s, self._decipher, strict=strict, quite=quite)


class GenericStreamCipher(GenericFunctionalCipher):

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
            except errors.IllegalAlphabetIndex as err:
                if quite:
                    q += 1
                    r.append(c)
                else:
                    raise err
        r = "".join(r)
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, f.__name__, s, r))
        return r


class GenericAlphabetCipher(GenericCipher):

    def __init__(self, alphabet=None, key=None):

        if alphabet is None:
            self._alphabet = alphabets.BasicAlphabet()
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


class GenericAlphabetStreamCipher(GenericAlphabetCipher, GenericStreamCipher):

    def __init__(self, alphabet=None, key=None):
        super().__init__(alphabet=alphabet, key=key)

    def pairs(self, s=None):
        s = s or self.alphabet.symbols
        c = self.encipher(s)
        return list(zip(s, c))

    def to_dataframe(self, s=None):
        return pd.DataFrame(self.pairs(s), columns=["clear", "encipher"])

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


class GenericIntegerAlphabetStreamCipher(GenericAlphabetStreamCipher):

    def __init__(self, alphabet=None, key=None):
        super().__init__(alphabet=alphabet, key=key)
        if not isinstance(self.alphabet, alphabets.IntegerAlphabet):
            raise errors.IllegalCipherParameter("Generic Stream Cypher requires Integer Alphabet.")


class GenericNaturalAlphabetStreamCipher(GenericIntegerAlphabetStreamCipher):

    def __init__(self, alphabet=None, key=None):
        super().__init__(alphabet=alphabet, key=key)
        if not self.alphabet.is_natural:
            raise errors.IllegalCipherParameter("Generic Stream Cypher requires Natural Alphabet.")


class GenericShapeCipher(GenericCipher):

    def __init__(self, shape=None, padding=" "):
        self._shape = shape
        self._padding = padding

    def __str__(self):
        return "<{} shape={} padding='{}'>".format(self.__class__.__name__, self.shape, self.padding)

    @property
    def shape(self):
        return self._shape

    @property
    def padding(self):
        return self._padding

    @abc.abstractmethod
    def _encipher(self, s, **kwargs):
        pass

    @abc.abstractmethod
    def _decipher(self, s, **kwargs):
        pass

    def _apply(self, s, f, shape=None, mode="auto", permutation=None):
        x = toolbox.Shaper.to_matrix(s, shape=shape or self.shape, mode=mode)
        r = f(x, shape=shape, mode=mode, permutation=permutation)
        r = toolbox.Shaper.to_str(r).rstrip()
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, f.__name__, s, r))
        return r

    def encipher(self, s, shape=None, mode="auto", permutation=None):
        return self._apply(s, self._encipher, shape=shape, mode=mode, permutation=permutation)

    def decipher(self, s, shape=None, mode="auto", permutation=None):
        return self._apply(s, self._decipher, shape=shape, mode=mode, permutation=permutation)


class GenericPermutationShapeCipher(GenericShapeCipher):

    def __init__(self, permutation, shape, padding=" "):
        super().__init__(shape=shape, padding=padding)
        self._permutation = permutation

    def __str__(self):
        return "<{} permutation={} shape={} padding='{}'>".format(self.__class__.__name__, self.permutation,
                                                                  self.shape, self.padding)

    @property
    def permutation(self):
        return self._permutation


class GenericCodexCipher(GenericCipher):
    pass


class GenericBaseCipher(GenericCipher):
    pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
