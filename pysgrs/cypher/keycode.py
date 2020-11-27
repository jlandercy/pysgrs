import sys

from pysgrs.settings import settings

from pysgrs.interfaces.cypher import GenericStreamCypher


class KeyCode(GenericStreamCypher):

    def __init__(self, key, alphabet=None):
        super().__init__(alphabet=alphabet, key=key)

    @property
    def key(self):
        return self._key

    def _cypher(self, c, k):
        x = self.alphabet.index(c)
        ck = self.key[k % self.keysize]
        y = self.alphabet.index(ck)
        print(c, x, ck, y)
        return (x + y) % self.alphabet.size

    def _decypher(self, c, k):
        return (self.alphabet.index(c) - self.alphabet.index(self.key[k % self.keysize])) % self.alphabet.size


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
