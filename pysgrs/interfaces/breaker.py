import abc
import sys

from pysgrs.interfaces.factory import CipherFactory
from pysgrs.toolbox import GenericScore
from pysgrs import errors
from pysgrs.settings import settings


class GenericBreaker(abc.ABC):

    def __init__(self, factory, score):

        if not isinstance(factory, CipherFactory):
            raise errors.IllegalParameter("Requires a CipherFactory, received {} instead".format(type(factory)))

        self._factory = factory

        if not isinstance(score, GenericScore):
            raise errors.IllegalParameter("Requires a Score, received {} instead".format(type(factory)))

        self._score = score

    @property
    def factory(self):
        return self._factory

    @property
    def score(self):
        return self._score


def main():
    settings.logger.warning("Hello world!")
    sys.exit(0)


if __name__ == "__main__":
    main()
