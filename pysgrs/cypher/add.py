import sys
import itertools

from pysgrs.settings import settings

from pysgrs.interfaces.cypher import GenericStreamCypher


class AddedKey(GenericStreamCypher):

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
    for i, k in enumerate(itertools.cycle("ABCD")):
        print(i, k)
        if i > 20:
            break

    sys.exit(0)


if __name__ == "__main__":
    main()
