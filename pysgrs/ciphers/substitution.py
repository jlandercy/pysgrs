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

    @property
    def offset(self):
        return self._offset

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

    def __init__(self, permutations=None, alphabet=None, auto=False):
        super().__init__(alphabet=alphabet)

        if permutations is None:
            if auto:
                #permutations = tuple(random.sample(tuple(range(self.alphabet.size)), self.alphabet.size)) # Pure PSL
                permutations = np.random.permutation(np.arange(self.alphabet.size))
            else:
                #permutations = tuple(range(self.alphabet.size))
                permutations = np.arange(self.alphabet.size)

        if len(permutations) != self.alphabet.size:
            raise errors.IllegalCypherParameter("Permutations (size={}) must have same size as {}".format(
                len(permutations), self))

        if not set(permutations) == set(self.alphabet.indices):
            raise errors.IllegalCypherParameter("Permutations {} must have compatible indices with {}".format(
                permutations, self))

        self._permutations = tuple(permutations)

    @property
    def permutations(self):
        return self._permutations

    def _encipher(self, c, k=None):
        return self.alphabet.symbol(self.permutations[self.alphabet.index(c)])

    def _decipher(self, c, k=None):
        return self.alphabet.symbol(self.permutations.index(self.alphabet.index(c)))


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
