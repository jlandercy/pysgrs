import sys

import numpy as np

from pysgrs.interfaces.cypher import GenericShapeCypher
from pysgrs.toolbox import Shaper
from pysgrs import errors
from pysgrs.settings import settings


class TranspositionCypher(GenericShapeCypher):

    def __init__(self, shape=None, padding=" "):
        super().__init__(shape=shape, padding=padding)

    def _cypher(self, x, **kwargs):
        return x.T

    def _decypher(self, x, **kwargs):
        #return x.T
        return self._cypher(x, **kwargs)


class ColumnPermutationCypher(GenericShapeCypher):

    def _cypher(self, s, permutation=None, shape=None, mode="auto"):
        return s

    def _decypher(self, s, permutation=None, shape=None, mode="auto"):
        return s


class RowPermutationCypher(GenericShapeCypher):

    def _cypher(self, s, permutation=None, shape=None, mode="auto"):
        return s

    def _decypher(self, s, permutation=None, shape=None, mode="auto"):
        return s


class ColumnCycleCypher(GenericShapeCypher):

    def _cypher(self, s, permutation=None, shape=None, mode="auto"):
        return s

    def _decypher(self, s, permutation=None, shape=None, mode="auto"):
        return s


class RowCycleCypher(GenericShapeCypher):

    def _cypher(self, s, permutation=None, shape=None, mode="auto"):
        return s

    def _decypher(self, s, permutation=None, shape=None, mode="auto"):
        return s


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
