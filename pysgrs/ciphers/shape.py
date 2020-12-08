import sys

import numpy as np
import pandas as pd

from pysgrs import ciphers
from pysgrs.toolbox import Shaper
from pysgrs import errors
from pysgrs.settings import settings


class TranspositionCipher(ciphers.GenericShapeCipher):

    def __init__(self, shape=None, padding=" "):
        super().__init__(shape=shape, padding=padding)

    def _encipher(self, x, **kwargs):
        return x.T

    def _decipher(self, x, **kwargs):
        return x.reshape(tuple(reversed(x.shape))).T


class ColumnPermutationCipher(ciphers.GenericPermutationShapeCipher):

    def _encipher(self, x, **kwargs):
        return pd.DataFrame(x).iloc[:, self.permutation].values

    def _decipher(self, x, **kwargs):
        return pd.DataFrame(x).iloc[:, np.argsort(self.permutation)].values


class RowPermutationCipher(ciphers.GenericPermutationShapeCipher):

    def _encipher(self, x, **kwargs):
        return pd.DataFrame(x).iloc[self.permutation, :].values

    def _decipher(self, x, **kwargs):
        return pd.DataFrame(x).iloc[np.argsort(self.permutation), :].values


class ColumnCycleCipher(ciphers.GenericPermutationShapeCipher):

    def _encipher(self, x, **kwargs):
        for i, n in enumerate(self.permutation):
            x[:, i] = np.roll(x[:, i], n)
        return x

    def _decipher(self, x, **kwargs):
        for i, n in enumerate(self.permutation):
            x[:, i] = np.roll(x[:, i], -n)
        return x


class RowCycleCipher(ciphers.GenericPermutationShapeCipher):

    def _encipher(self, x, **kwargs):
        for i, n in enumerate(self.permutation):
            x[i, :] = np.roll(x[i, :], n)
        return x

    def _decipher(self, x, **kwargs):
        for i, n in enumerate(self.permutation):
            x[i, :] = np.roll(x[i, :], -n)
        return x


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
