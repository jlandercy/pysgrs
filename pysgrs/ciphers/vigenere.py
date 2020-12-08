import sys

from pysgrs.settings import settings

from pysgrs.interfaces.cipher import GenericNaturalAlphabetStreamCipher


class VigenereCipher(GenericNaturalAlphabetStreamCipher):

    def __init__(self, key, alphabet=None):
        super().__init__(alphabet=alphabet, key=key)

    def _encipher(self, c, k):
        return self.alphabet.symbol(
            (self.alphabet.index(c) + self.alphabet.index(self.key[k % self.keysize])) % self.alphabet.size
        )

    def _decipher(self, c, k):
        return self.alphabet.symbol(
            (self.alphabet.index(c) - self.alphabet.index(self.key[k % self.keysize])) % self.alphabet.size
        )


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
