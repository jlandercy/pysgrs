import sys
import itertools

import numpy as np
import pandas as pd

from pysgrs.interfaces.cypher import GenericShapeCypher
from pysgrs.settings import settings


class TranspositionCypher(GenericShapeCypher):

    def __init__(self, shape=None):
        super().__init__(shape=shape)

    def shaper(self, n):
        m = np.sqrt(n)
        m0 = int(np.floor(m))
        m1 = int(np.ceil(m))
        df = pd.DataFrame(itertools.product([m0, m1], [m0, m1]), columns=["nrow", "ncol"])
        df["size"] = df["nrow"]*df["ncol"]
        df["padding"] = df["size"] - n
        return df

    def cypher(self, s, shape=None):
        shape = shape or self.shape
        n = len(s)
        print(self.shaper(n))

    def decypher(self, s):
        pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
