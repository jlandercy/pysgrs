import sys
import itertools

import numpy as np
import pandas as pd

from pysgrs.interfaces.cypher import GenericShapeCypher
from pysgrs import errors
from pysgrs.settings import settings


class TranspositionCypher(GenericShapeCypher):

    def __init__(self, shape=None, pad=" "):
        super().__init__(shape=shape)

    def get_shapes(self, s, shape=None):
        n = len(s)
        m = np.sqrt(n)
        mmin = int(np.floor(m))
        mmax = int(np.ceil(m))
        shapes = [
            {"id": "lowsquare", "shape": (mmin, mmin)},
            {"id": "lowrect", "shape": (mmin, mmax)},
            {"id": "uprect", "shape": (mmax, mmin)},
            {"id": "upsquare", "shape": (mmax, mmax)},
        ]
        if shape:
            shapes.append({"id": "user", "shape": shape})
        if self.shape:
            shapes.append({"id": "default", "shape": self.shape})
        df = pd.DataFrame(shapes)
        df["size"] = df["shape"].apply(np.prod)
        df["padding"] = df["size"] - n
        df["valid"] = df["padding"] >= 0
        df = df.set_index("id")
        mopt = df.loc[df["valid"], "padding"].min()
        df.loc["auto", :] = df.loc[df["padding"] == mopt, :].iloc[0, :]
        return df

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
