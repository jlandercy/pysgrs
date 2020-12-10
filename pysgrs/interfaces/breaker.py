import abc
import sys

from pysgrs.interfaces.score import GenericScore
from pysgrs import errors
from pysgrs.settings import settings


class GenericBreaker(abc.ABC):

    def __init__(self, score):

        if not isinstance(score, GenericScore):
            raise errors.IllegalParameter("Requires a Score, received {} instead".format(type(factory)))

        self._score = score

    @property
    def score(self):
        return self._score

    @abc.abstractmethod
    def attack(self, text, **kwargs):
        pass

    @abc.abstractmethod
    def analyze(self, text, **kwargs):
        pass

    @abc.abstractmethod
    def guess(self, text, **kwargs):
        pass


def main():
    settings.logger.warning("Hello world!")
    sys.exit(0)


if __name__ == "__main__":
    main()
