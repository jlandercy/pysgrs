import sys

import numpy as np

from pysgrs.interfaces.cypher import GenericShapeCypher
from pysgrs import errors
from pysgrs.settings import settings


class TranspositionCypher(GenericShapeCypher):

    def __init__(self, shape=None, pad=" "):
        super().__init__(shape=shape)

    def cypher(self, s, shape=None, mode="auto"):
        shapes = self.get_shapes(s, shape=shape)
        shape = shapes.loc[mode, :]
        if shape["valid"]:
            s += self.pad*int(shape["padding"])
            x = np.array(list(s)).reshape(shape["shape"])
            return "".join(x.T.flatten()).rstrip()
        else:
            raise errors.IllegalCypherParameter("Invalid shape: {}".format(shape.to_dict()))

    def decypher(self, s, shape=None, mode="auto"):
        shapes = self.get_shapes(s, shape=shape)
        shape = shapes.loc[mode, :]
        shape = tuple(reversed(shape["shape"]))
        return self.cypher(s, shape=shape, mode="user")


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
