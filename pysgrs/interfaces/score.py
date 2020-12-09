import abc
import sys
import collections
import pathlib
import json

import numpy as np

from pysgrs.settings import settings
from pysgrs import errors
from pysgrs.toolbox.cleaner import AsciiCleaner


class GenericScore(abc.ABC):

    @abc.abstractmethod
    def score(self, text, **kwargs):
        pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
