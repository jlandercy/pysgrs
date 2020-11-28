import sys

from pysgrs.interfaces.cypher import GenericShapeCypher
from pysgrs.settings import settings


class TranspositionCypher(GenericShapeCypher):

    def __init__(self, shape=None):
        super().__init__(shape=shape)

    def cypher(self, s):
        pass

    def decypher(self, s):
        pass



def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
