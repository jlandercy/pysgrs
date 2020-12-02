import sys

import numpy as np

from pysgrs.interfaces.cypher import GenericShapeCypher
from pysgrs.toolbox import Shaper
from pysgrs import errors
from pysgrs.settings import settings


class TranspositionCypher(GenericShapeCypher):

    def __init__(self, shape=None, padding=" "):
        super().__init__(shape=shape, padding=padding)

    def _transform(self, s, shape):
        r = "".join(Shaper.to_matrix(s, shape).T.flatten()).rstrip()
        settings.logger.debug("{}.{}('{}', {}) -> '{}'".format(self, "_transform", s, shape, r))
        return r

    def cypher(self, s, shape=None, mode="auto"):
        shape = shape or self.get_shapes(s, shape=shape).loc[mode, "shape"]
        r = self._transform(s, shape)
        return r

    def decypher(self, s, shape=None, mode="auto"):
        shape = shape or self.get_shapes(s, shape=shape).loc[mode, "shape"]
        r = self._transform(s, tuple(reversed(shape)))
        return r


class ColumnPermutationCypher(GenericShapeCypher):

    def cypher(self, s, permutation, shape=None, mode="auto"):
        pass

    def decypher(self, s, permutation, shape=None, mode="auto"):
        pass


class RowPermutationCypher(GenericShapeCypher):

    def cypher(self, s, permutation, shape=None, mode="auto"):
        pass

    def decypher(self, s, permutation, shape=None, mode="auto"):
        pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
