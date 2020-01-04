import sys
#import abc

import numpy as np

#from pysgrs.settings import settings


class GenericAlphabet:

    def __init__(self, alphabet):

        if isinstance(alphabet, str):
            assert len(set(alphabet)) == len(alphabet)
            self._alphabet = alphabet

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def n(self):
        return len(self.alphabet)

    def index(self, c):
        return self.alphabet.index(c)

    def digit(self, i):
        return self.alphabet[i]

    def encode(self, s):
        return [self.index(c) for c in s]

    def decode(self, l, sep=""):
        return sep.join([self.digit(i) for i in l])

    @property
    def direct(self):
        return {c: self.index(c) for c in self.alphabet}

    @property
    def inverse(self):
        return {i: c for (c, i) in self.direct.items()}


class Alphabet(GenericAlphabet):

    _offset = 65

    def __init__(self):
        super().__init__("".join([chr(x + Alphabet._offset) for x in range(26)]))

    def index(self, c):
        return ord(c) - Alphabet._offset

    def digit(self, i):
        return chr(i + Alphabet._offset)


class Cypher:

    def __init__(self, alphabet=None, offset=0):

        self._offset = offset
        if alphabet is None:
            self._alphabet = Alphabet()

    @property
    def offset(self):
        return self._offset

    @property
    def alphabet(self):
        return self._alphabet

    def _cypher(self, x):
        return (x + self.offset) % self.alphabet.n

    def _decypher(self, x):
        return (x - self.offset) % self.alphabet.n

    def cypher(self, s):
        return self.alphabet.decode(self._cypher(np.array(self.alphabet.encode(s))))

    def decypher(self, s):
        return self.alphabet.decode(self._decypher(np.array(self.alphabet.encode(s))))


def main():

    sys.exit(0)


if __name__ == "__main__":
    main()
