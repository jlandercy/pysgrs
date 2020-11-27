import sys

from pysgrs.settings import settings

from pysgrs.interfaces.cypher import GenericStreamCypher


class KeyCypher(GenericStreamCypher):

    def __init__(self, key, alphabet=None):
        super().__init__(alphabet=alphabet, key=key)

    def _cypher(self, c, k):
        return self.alphabet.digit(
            (self.alphabet.index(c) + self.alphabet.index(self.key[k % self.keysize])) % self.alphabet.size)

    def _decypher(self, c, k):
        return self.alphabet.digit(
            (self.alphabet.index(c) - self.alphabet.index(self.key[k % self.keysize])) % self.alphabet.size)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
