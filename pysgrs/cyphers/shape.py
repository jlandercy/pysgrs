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
        return x.T


class ColumnPermutationCypher(GenericShapeCypher):

    def _cypher(self, s, permutation, shape=None, mode="auto"):
        pass

    def _decypher(self, s, permutation, shape=None, mode="auto"):
        pass


class RowPermutationCypher(GenericShapeCypher):

    def _cypher(self, s, permutation, shape=None, mode="auto"):
        pass

    def _decypher(self, s, permutation, shape=None, mode="auto"):
        pass


class ColumnCycleCypher(GenericShapeCypher):

    def _cypher(self, s, permutation, shape=None, mode="auto"):
        pass

    def _decypher(self, s, permutation, shape=None, mode="auto"):
        pass


class RowCycleCypher(GenericShapeCypher):

    def _cypher(self, s, permutation, shape=None, mode="auto"):
        pass

    def _decypher(self, s, permutation, shape=None, mode="auto"):
        pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
