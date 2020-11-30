import sys

from pysgrs.settings import settings

from pysgrs import alphabets
from pysgrs import errors


class AsciiAlphabet(alphabets.GenericIntegerAlphabet):

    def __init__(self, offset=32, size=95, natural=False):
        if natural:
            super().__init__("".join([chr(x + offset) for x in range(size)]))
            self._offset = offset
        else:
            super().__init__("".join([chr(x + offset) for x in range(size)]), indices=range(offset, offset+size))
            self._offset = 0

    @property
    def offset(self):
        return self._offset

    def index(self, c):
        if 0 <= ord(c) - self.offset < self.size:
            return ord(c) - self.offset
        else:
            raise errors.IllegalAlphabetIndex("Symbol <{}> outside allowed range of {}".format(c, self))

    def symbol(self, k):
        if 0 <= k < self.size:
            return chr(k + self.offset)
        else:
            raise errors.IllegalAlphabetIndex("Index <{}> outside allowed range of {}".format(k, self))


class SimpleAlphabet(AsciiAlphabet):

    def __init__(self):
        super().__init__(offset=65, size=26, natural=True)


class BinaryAlphabet(alphabets.GenericIntegerAlphabet):

    def __init__(self):
        super().__init__("AB")


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
