import sys

from pysgrs.settings import settings

import numpy as np
import pandas as pd


class Shaper:

    @staticmethod
    def get_shapes(n, shape=None):
        # Explore:
        m = np.sqrt(n)
        mmin = int(np.floor(m))
        mmax = int(np.ceil(m))
        shapes = [
            {"id": "minsquare", "shape": (mmin, mmin)},
            {"id": "minmaxrect", "shape": (mmin, mmax)},
            {"id": "maxsquare", "shape": (mmax, mmax)},
        ]
        if shape:
            shapes.append({"id": "user", "shape": shape})
        for i in range(2, n):
            shapes.append({"id": "rect-{:d}".format(i), "shape": (i, int(np.ceil(n/i)))})
        df = pd.DataFrame(shapes)
        # Arrange:
        df["size"] = df["shape"].apply(np.prod)
        df["padding"] = df["size"] - n
        df["factor"] = df["shape"].apply(lambda x: np.abs(x[0] - x[1]))
        df = df.set_index("id")
        df = df.sort_values(["padding", "factor"])
        return df

    @staticmethod
    def squeeze(x):
        return np.array(x).reshape(-1, 1).squeeze()


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
