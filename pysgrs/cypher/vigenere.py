import sys

from pysgrs.settings import settings

from pysgrs.interfaces.cypher import GenericStreamCypher


class Vigenere(GenericStreamCypher):

    def __init__(self, key, alphabet=None):
        super().__init__(alphabet=alphabet, key=key)

    def _cypher(self, c, k):
        pass

    def _decypher(self, c, k):
        pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
