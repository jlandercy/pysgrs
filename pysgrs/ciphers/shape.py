import sys

import numpy as np
import pandas as pd

from pysgrs import ciphers
from pysgrs.toolbox import Shaper
from pysgrs import errors
from pysgrs.settings import settings


class TranspositionCypher(ciphers.GenericShapeCipher):

    def __init__(self, shape=None, padding=" "):
        super().__init__(shape=shape, padding=padding)

    def _cypher(self, x, **kwargs):
        return x.T

    def _decypher(self, x, **kwargs):
        return x.reshape(tuple(reversed(x.shape))).T


class ColumnPermutationCypher(ciphers.GenericPermutationShapeCypher):

    def _cypher(self, x, **kwargs):
        return pd.DataFrame(x).iloc[:, self.permutation].values

    def _decypher(self, x, **kwargs):
        return pd.DataFrame(x).iloc[:, np.argsort(self.permutation)].values


class RowPermutationCypher(ciphers.GenericPermutationShapeCypher):

    def _cypher(self, x, **kwargs):
        return pd.DataFrame(x).iloc[self.permutation, :].values

    def _decypher(self, x, **kwargs):
        return pd.DataFrame(x).iloc[np.argsort(self.permutation), :].values


class ColumnCycleCypher(ciphers.GenericPermutationShapeCypher):

    def _cypher(self, x, **kwargs):
        for i, n in enumerate(self.permutation):
            x[:, i] = np.roll(x[:, i], n)
        return x

    def _decypher(self, x, **kwargs):
        for i, n in enumerate(self.permutation):
            x[:, i] = np.roll(x[:, i], -n)
        return x


class RowCycleCypher(ciphers.GenericPermutationShapeCypher):

    def _cypher(self, x, **kwargs):
        for i, n in enumerate(self.permutation):
            x[i, :] = np.roll(x[i, :], n)
        return x

    def _decypher(self, x, **kwargs):
        for i, n in enumerate(self.permutation):
            x[i, :] = np.roll(x[i, :], -n)
        return x


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
