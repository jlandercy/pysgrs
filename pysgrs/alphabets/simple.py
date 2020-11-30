import sys

from pysgrs.settings import settings

from pysgrs import alphabets
from pysgrs import errors


class SimpleAlphabet(alphabets.GenericMixedAlphabet):
    """
    Base SimpleAlphabet [A-Z]:
    Using commodities from Generic SimpleAlphabet but replacing indexing by ASCII index manipulation for efficiency sake.
    """

    def __init__(self, offset=65, size=26):
        super().__init__("".join([chr(x + offset) for x in range(size)]))
        self._offset = offset

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


class BinaryAlphabet(alphabets.GenericIntegerAlphabet):

    def __init__(self):
        super().__init__("AB")


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
