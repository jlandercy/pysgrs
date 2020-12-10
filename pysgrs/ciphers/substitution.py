import sys
#import random

import numpy as np

from pysgrs.interfaces import cipher
from pysgrs.toolbox import ModularArithmetic
from pysgrs import errors


class AlphabetCipher(cipher.GenericAlphabetStreamCipher):

    def __init__(self, alphabet=None):
        super().__init__(alphabet=alphabet)

    def _encipher(self, c, k=None):
        return self.alphabet.index(c)

    def _decipher(self, c, k=None):
        return self.alphabet.symbol(c)


class RotationCipher(cipher.GenericNaturalAlphabetStreamCipher):

    def __init__(self, alphabet=None, offset=3):
        super().__init__(alphabet=alphabet)
        self._offset = offset

    def __str__(self):
        return "<{} offset={} alphabet={}>".format(self.__class__.__name__, self._offset, self.alphabet)

    @property
    def offset(self):
        return self._offset

    def configuration(self):
        c = super().configuration()
        c.update({"offset": self.offset})
        return c

    def _encipher(self, c, k=None):
        return self.alphabet.symbol((self.alphabet.index(c) + self.offset) % self.alphabet.size)

    def _decipher(self, c, k=None):
        return self.alphabet.symbol((self.alphabet.index(c) - self.offset) % self.alphabet.size)


class CaesarCipher(RotationCipher):

    def __init__(self, alphabet=None):
        super().__init__(alphabet=alphabet, offset=3)


class ReversedCipher(cipher.GenericNaturalAlphabetStreamCipher):

    def __init__(self, alphabet=None):
        super().__init__(alphabet=alphabet)

    def _encipher(self, c, k=None):
        return self.alphabet.symbol(self.alphabet.size - self.alphabet.index(c) - 1)

    def _decipher(self, c, k=None):
        return self.alphabet.symbol(self.alphabet.size - self.alphabet.index(c) - 1)


class PermutationCipher(cipher.GenericNaturalAlphabetStreamCipher):

    def __init__(self, permutation=None, alphabet=None, auto=False):
        super().__init__(alphabet=alphabet)

        if permutation is None:
            if auto:
                #permutation = tuple(random.sample(tuple(range(self.alphabet.size)), self.alphabet.size)) # Pure PSL
                permutation = np.random.permutation(np.arange(self.alphabet.size))
            else:
                #permutation = tuple(range(self.alphabet.size))
                permutation = np.arange(self.alphabet.size)

        if len(permutation) != self.alphabet.size:
            raise errors.IllegalCipherParameter("Permutations (size={}) must have same size as {}".format(
                len(permutation), self))

        if not set(permutation) == set(self.alphabet.indices):
            raise errors.IllegalCipherParameter("Permutations {} must have compatible indices with {}".format(
                permutation, self))

        self._permutation = tuple(permutation)
        self._permutation_inverse = tuple(np.argsort(self.permutation))

    @property
    def permutation(self):
        return self._permutation

    @property
    def permutation_inverse(self):
        return self._permutation_inverse

    def _encipher(self, c, k=None):
        return self.alphabet.symbol(self.permutation[self.alphabet.index(c)])

    def _decipher(self, c, k=None):
        #return self.alphabet.symbol(self.permutation.index(self.alphabet.index(c)))
        return self.alphabet.symbol(self.permutation_inverse[self.alphabet.index(c)])


class AffineCipher(cipher.GenericNaturalAlphabetStreamCipher):

    def __init__(self, a=5, b=8, alphabet=None):
        super().__init__(alphabet=alphabet)
        self._a = a
        self._b = b
        self._a_inverse = ModularArithmetic.modinv(self.a, self.alphabet.size)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def a_inverse(self):
        return self._a_inverse

    def _encipher(self, c, k=None):
        return self.alphabet.symbol((self.a*self.alphabet.index(c) + self.b) % self.alphabet.size)

    def _decipher(self, c, k=None):
        return self.alphabet.symbol((self.a_inverse*(self.alphabet.index(c) - self.b)) % self.alphabet.size)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
