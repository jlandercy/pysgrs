import sys

import numpy as np
import pandas as pd

from pysgrs import errors
from pysgrs.settings import settings


class Shaper:

    @staticmethod
    def get_shapes(n, shape=None):
        # Explore:
        m = np.sqrt(n)
        mmin = int(np.floor(m))
        mmax = int(np.ceil(m))
        shapes = [
            {"id": "min-square", "shape": (mmin, mmin)},
            {"id": "opt-rect", "shape": (mmin, mmax)},
            {"id": "opt-rect-2", "shape": (mmax, mmin)},
            {"id": "max-square", "shape": (mmax, mmax)},
        ]
        if shape:
            shapes.append({"id": "user", "shape": shape})
        for i in range(2, n):
            shapes.append({"id": "rect-{:d}".format(i), "shape": (i, int(np.ceil(n/i)))})
        df = pd.DataFrame(shapes)
        # Arrange:
        df["size"] = df["shape"].apply(np.prod)
        df["padding"] = df["size"] - n
        df["shape_diff"] = df["shape"].apply(lambda x: np.abs(x[0] - x[1]))
        df["score"] = (((1/2 + df["padding"])/n)**3)*(1 + df["shape_diff"]**4)
        df = df.set_index("id")
        df = df.sort_values(["score", "padding", "shape_diff"])
        df.loc["auto", :] = df.loc[(df["score"] > 0) & (df.index.str.contains("-square|-rect")), :].iloc[0, :]
        df = df.sort_values(["score", "padding", "shape_diff"])
        return df

    @staticmethod
    def pad(s, n, padding=" "):
        m = n - len(s)
        if m >= 0:
            return s + padding*m
        else:
            raise errors.IllegalParameter(
                "Final size (n={}) must be greater or equal to string length ({})".format(n, len(s)))

    @staticmethod
    def shape(s, shape, padding=" "):
        n = np.prod(shape)
        s = Shaper.pad(s, n, padding=padding)
        x = np.array(list(s)).reshape(shape)
        return x

    @staticmethod
    def flatten(x):
        return np.array(x).flatten()


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
