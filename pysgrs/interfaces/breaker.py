import abc
import sys
import copy

from pysgrs.interfaces.score import GenericScore
from pysgrs import errors
from pysgrs.settings import settings


class GenericState:

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def __str__(self):
        return "<{} state={}>".format(self.__class__.__name__, self.__dict__)

    def update(self, **kwargs):
        self.__dict__.update(**kwargs)
        return self

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]

    def copy(self):
        return GenericState(**self.to_dict())

    def log(self, message="State: ", log_format="{message:}{full_state:}", **kwargs):
        state = self.to_dict()
        settings.logger.debug(log_format.format(message=message, full_state=state, **state, **kwargs))


class BreakerState(GenericState):
    pass


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


class GenericLocalSearchBreaker(GenericBreaker):

    def __init__(self, score):
        super().__init__(score)
        self._current_state = None

    @property
    def current_state(self):
        return self._current_state

    @abc.abstractmethod
    def _initial_state(self, **kwargs):
        pass

    @abc.abstractmethod
    def _next_state(self, **kwargs):
        pass

    @abc.abstractmethod
    def _score_state(self, **kwargs):
        pass


def main():
    settings.logger.warning("Hello world!")
    sys.exit(0)


if __name__ == "__main__":
    main()
