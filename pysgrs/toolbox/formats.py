import sys

from pysgrs.settings import settings

import numpy as np
import pandas as pd


class Shaper:

    @staticmethod
    def get_shapes(s, shape=None):
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
        df = pd.DataFrame(shapes)
        df["size"] = df["shape"].apply(np.prod)
        df["padding"] = df["size"] - n
        df["valid"] = df["padding"] >= 0
        df = df.set_index("id")
        mopt = df.loc[df["valid"], "padding"].min()
        df.loc["auto", :] = df.loc[df["padding"] == mopt, :].iloc[0, :]
        return df

    @staticmethod
    def squeeze(x):
        return np.array(x).reshape(-1, 1).squeeze()


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
