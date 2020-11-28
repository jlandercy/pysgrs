import sys
import random

from pysgrs.interfaces.cypher import GenericStreamCypher
from pysgrs import errors


class RotationCypher(GenericStreamCypher):

    def __init__(self, alphabet=None, offset=3):
        super().__init__(alphabet=alphabet)
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    def _cypher(self, c, k=None):
        return self.alphabet.symbol((self.alphabet.index(c) + self.offset) % self.alphabet.size)

    def _decypher(self, c, k=None):
        return self.alphabet.symbol((self.alphabet.index(c) - self.offset) % self.alphabet.size)


class CaesarCypher(RotationCypher):

    def __init__(self, alphabet=None):
        super().__init__(alphabet=alphabet, offset=3)


class ReversedCypher(GenericStreamCypher):

    def __init__(self, alphabet=None):
        super().__init__(alphabet=alphabet)

    def _cypher(self, c, k=None):
        return self.alphabet.symbol(self.alphabet.size - self.alphabet.index(c) - 1)

    def _decypher(self, c, k=None):
        return self.alphabet.symbol(self.alphabet.size - self.alphabet.index(c) - 1)


class PermutationCypher(GenericStreamCypher):

    def __init__(self, permutations=None, alphabet=None, auto=False):
        super().__init__(alphabet=alphabet)

        if permutations is None:
            if auto:
                permutations = tuple(random.sample(range(self.alphabet.size), self.alphabet.size))
            else:
                permutations = tuple(range(self.alphabet.size))

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

    def _cypher(self, c, k=None):
        return self.alphabet.symbol(self.permutations[self.alphabet.index(c)])

    def _decypher(self, c, k=None):
        return self.alphabet.symbol(self.permutations.index(self.alphabet.index(c)))


class AffineCypher(GenericStreamCypher):

    def __init__(self, a=5, b=8, alphabet=None):
        super().__init__(alphabet=alphabet)
        self._a = a
        self._b = b
        self.ainv

    @staticmethod
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = AffineCypher.egcd(b % a, a)
            return g, x - (b // a) * y, y

    @staticmethod
    def modinv(a, m):
        g, x, y = AffineCypher.egcd(a, m)
        if g != 1:
            raise errors.IllegalCypherParameter('Modular inverse does not exist for {} mod {}'.format(a, m))
        else:
            return x % m

    @property
    def a(self):
        return self._a

    @property
    def ainv(self):
        #return pow(self.a, -1, self.alphabet.size) # Only Python 3.8+
        return AffineCypher.modinv(self.a, self.alphabet.size)

    @property
    def b(self):
        return self._b

    def _cypher(self, c, k=None):
        return self.alphabet.symbol((self.a*self.alphabet.index(c) + self.b) % self.alphabet.size)

    def _decypher(self, c, k=None):
        return self.alphabet.symbol((self.ainv*(self.alphabet.index(c) - self.b)) % self.alphabet.size)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
