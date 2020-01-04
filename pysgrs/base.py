import sys
import abc

import numpy as np

from pysgrs.settings import settings


class GenericAlphabet(abc.ABC):

    def __init__(self, alphabet):

        if isinstance(alphabet, str):
            self._alphabet = alphabet

    @abc.abstractmethod
    def index(self, c):
        pass

    @abc.abstractmethod
    def digit(self, i):
        pass

    @abc.abstractmethod
    def encode(self, s):
        pass

    @abc.abstractmethod
    def decode(self, l):
        pass

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def n(self):
        return len(self.alphabet)


class Alphabet(GenericAlphabet):

    _ascii_offset = 65

    def __init__(self, offset=1):
        super().__init__("".join([chr(x + Alphabet._ascii_offset) for x in range(26)]))
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    def index(self, c):
        return ord(c) - Alphabet._ascii_offset + self._offset

    def digit(self, i):
        return chr(i + Alphabet._ascii_offset + self._offset)

    def encode(self, s):
        return [self.index(c) for c in s]

    def decode(self, l, sep=""):
        return sep.join([self.digit(i) for i in l])


class Cypher:

    def __init__(self, alphabet=None):
        if alphabet is None:
            self._alphabet = Alphabet()

    @property
    def alphabet(self):
        return self._alphabet

    def _cypher(self, x):
        return ((x + 3) % self.alphabet.n) - self.alphabet.offset

    def _decypher(self, x):
        return ((x - 3) % self.alphabet.n) #+ self.alphabet.offset

    def cypher(self, s):
        return self.alphabet.decode(self._cypher(np.array(self.alphabet.encode(s))))

    def decypher(self, s):
        return self.alphabet.decode(self._decypher(np.array(self.alphabet.encode(s))))

    def codex(self):
        x = self.alphabet.alphabet
        y = self.cypher(x)
        z = self.decypher(y)
        print(x, y, z)



def main():

    A = Alphabet()
    print(A.encode("ABCDEFG"))
    print(A.decode([1, 2, 3, 4, 5, 6, 7]))

    C = Cypher()
    print(C.cypher("ABCDEF"))
    C.codex()

    sys.exit(0)


if __name__ == "__main__":
    main()
