import sys

from pysgrs.settings import settings

from pysgrs.interfaces.cypher import GenericStreamCypher


class RotationCypher(GenericStreamCypher):

    def __init__(self, alphabet=None, offset=3):
        super().__init__(alphabet=alphabet)
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    def _cypher(self, c, k=None):
        return self.alphabet.digit((self.alphabet.index(c) + self.offset) % self.alphabet.size)

    def _decypher(self, c, k=None):
        return self.alphabet.digit((self.alphabet.index(c) - self.offset) % self.alphabet.size)


class CaesarCypher(RotationCypher):

    def __init__(self, alphabet=None):
        super().__init__(alphabet=alphabet, offset=3)


class ReversedCypher(GenericStreamCypher):

    def __init__(self, alphabet=None):
        super().__init__(alphabet=alphabet)

    def _cypher(self, c, k=None):
        return self.alphabet.digit(self.alphabet.size - self.alphabet.index(c) - 1)

    def _decypher(self, c, k=None):
        return self.alphabet.digit(self.alphabet.size - self.alphabet.index(c) - 1)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()