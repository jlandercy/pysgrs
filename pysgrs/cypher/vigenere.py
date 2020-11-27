import sys

from pysgrs.settings import settings

from pysgrs.interfaces.cypher import GenericStreamCypher


class Vigenere(GenericStreamCypher):

    def __init__(self, key, alphabet=None):
        super().__init__(alphabet=alphabet)
        self._key = key

    @property
    def key(self):
        return self._key

    def _cypher(self, x):
        return (x + self.offset) % self.alphabet.n

    def _decypher(self, x):
        return (x - self.offset) % self.alphabet.n


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
