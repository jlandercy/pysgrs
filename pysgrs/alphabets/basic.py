import sys

from pysgrs import alphabets
from pysgrs import errors
from pysgrs.settings import settings


class AsciiAlphabet(alphabets.GenericIntegerAlphabet):

    def __init__(self, offset=32, size=95, natural=False):
        if natural:
            super().__init__("".join([chr(x + offset) for x in range(size)]))
            self._offset = offset
            self._start = 0
            self._stop = size
        else:
            super().__init__("".join([chr(x + offset) for x in range(size)]), indices=range(offset, offset + size))
            self._offset = 0
            self._start = offset
            self._stop = offset + size

    @property
    def offset(self):
        return self._offset

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    def index(self, c):
        if self.start <= ord(c) - self.offset < self.stop:
            return ord(c) - self.offset
        else:
            raise errors.IllegalAlphabetIndex("Symbol <{}> outside allowed range of {}".format(c, self))

    def symbol(self, k):
        if self.start <= k < self.stop:
            return chr(k + self.offset)
        else:
            raise errors.IllegalAlphabetIndex("Index <{}> outside allowed range of {}".format(k, self))


class BasicAlphabet(AsciiAlphabet):

    def __init__(self):
        super().__init__(offset=65, size=26, natural=True)


class BinaryAlphabet(alphabets.GenericIntegerAlphabet):

    def __init__(self):
        super().__init__("AB")


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
