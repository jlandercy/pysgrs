import sys

from pysgrs.settings import settings

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

    def __init__(self, permutations, alphabet=None):
        super().__init__(alphabet=alphabet)

        if len(permutations) != self.alphabet.size:
            raise errors.IllegalCypherParameter("Permutation (size={}) must have same size as {}".format(
                len(permutations), self))

        self._permutations = tuple(permutations)

    @property
    def permutations(self):
        return self._permutations

    def _cypher(self, c, k=None):
        return self.alphabet.symbol(self.alphabet.size - self.alphabet.index(c) - 1)

    def _decypher(self, c, k=None):
        return self.alphabet.symbol(self.alphabet.size - self.alphabet.index(c) - 1)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
