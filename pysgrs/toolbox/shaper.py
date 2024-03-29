import sys
from collections.abc import Iterable

import numpy as np
import pandas as pd

from pysgrs import errors
from pysgrs.settings import settings


class Shaper:

    @staticmethod
    def get_shapes(n, shape=None, score=None):

        def _score(x):
            return (((1/2 + x["padding"])/n)**3)*(1 + x["shape_diff"]**4)

        score = score or _score

        # Explore:
        m = np.sqrt(n)
        mmin = int(np.floor(m))
        mmax = int(np.ceil(m))
        shapes = [
            {"id": "min-square", "shape": (mmin, mmin)},
            {"id": "opt-rect-1", "shape": (mmin, mmax)},
            {"id": "opt-rect-2", "shape": (mmax, mmin)},
            {"id": "max-square", "shape": (mmax, mmax)},
        ]
        if shape:
            modekey = "user"
            shapes.append({"id": modekey, "shape": shape})
        else:
            modekey = "auto"
        for i in range(2, n):
            shapes.append({"id": "rect-{:d}".format(i), "shape": (i, int(np.ceil(n/i)))})
        df = pd.DataFrame(shapes)

        # Arrange:
        df["size"] = df["shape"].apply(np.prod)
        df["padding"] = df["size"] - n
        df["shape_diff"] = df["shape"].apply(lambda x: np.abs(x[0] - x[1]))
        df["score"] = df.apply(score, axis=1)
        df = df.set_index("id")
        df = df.sort_values(["score", "padding", "shape_diff"])
        df.loc["auto", :] = df.loc[(df["score"] > 0) & (df.index.str.contains("-square|-rect")), :].iloc[0, :]
        df = df.sort_values(["score", "padding", "shape_diff"])

        settings.logger.debug("Shaper: {}={}".format(modekey, df.loc[modekey].to_dict()))

        return df

    @staticmethod
    def pad(s, n, padding=" "):
        m = n - len(s)
        if m >= 0:
            settings.logger.debug("Shaper: {}-pad string of length {} with '{}'".format(m, len(s), padding))
            return s + padding*m
        else:
            raise errors.IllegalParameter(
                "Final size (max_ngram={}) must be greater or equal to string length ({})".format(n, len(s)))

    @staticmethod
    def to_matrix(s, shape=None, mode="auto", padding=" ", row_separator="\n"):
        if isinstance(s, str):
            if shape:
                s = s.replace(row_separator, "")
            if row_separator in s:
                x = s.split(row_separator)
                x[-1] = Shaper.pad(x[-1], len(x[0]), padding=padding)
                x = [list(t) for t in x]
                if not all([len(s) == len(x[0]) for s in x]):
                    raise errors.IllegalParameter(
                        "All rows must have the same length unless the last which may be padded")
            else:
                shape = shape or Shaper.get_shapes(len(s), shape=shape).loc[mode, "shape"]
                n = np.prod(shape)
                s = Shaper.pad(s, n, padding=padding)
                x = list(s)
            x = np.array(x)
        elif isinstance(s, Iterable):
            x = np.array(s)
        else:
            raise errors.IllegalParameter("String or array expected, received {} instead".format(type(s)))
        if len(x.shape) < 2 or shape:
            x = x.reshape(shape)
        settings.logger.debug("Shaper: {} of size {} shaped to {}-matrix.".format(type(s), len(s), x.shape))
        return x

    @staticmethod
    def to_vector(x):
        return np.array(x).flatten()

    @staticmethod
    def to_str(x):
        return "".join(Shaper.to_vector(x))


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
