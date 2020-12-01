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
        return "".join(Shaper.shape(s, shape).T.flatten()).rstrip()

    def cypher(self, s, shape=None, mode="auto"):
        shape = shape or self.get_shapes(s, shape=shape).loc[mode, "shape"]
        r = self._transform(s, shape)
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, "cypher", s, r))
        return r

    def decypher(self, s, shape=None, mode="auto"):
        shape = shape or self.get_shapes(s, shape=shape).loc[mode, "shape"]
        r = self._transform(s, tuple(reversed(shape)))
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, "decypher", s, r))
        return r


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
