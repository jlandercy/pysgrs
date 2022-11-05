import abc
import collections
import pathlib
import json

import numpy as np

from pysgrs.settings import settings
from pysgrs import errors


class GenericSpace(abc.ABC):

    @abc.abstractmethod
    def generate(self, **kwargs):
        pass

    @abc.abstractmethod
    def sample(self, size=1):
        pass

    def size(self):
        count = 0
        for _ in self.generate():
            count += 1
        return count
