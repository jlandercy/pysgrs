import sys
import copy

from pysgrs import cyphers
from pysgrs import errors
from pysgrs.settings import settings


class PipelineCypher(cyphers.GenericCypher):

    def __init__(self, pipeline, **kwargs):
        if not all([isinstance(c, cyphers.GenericCypher) for c in pipeline]):
            raise errors.IllegalCypherParameter(
                "Pipeline must be a sequence of cyphers, received {} instead.".format(pipeline))
        self._pipeline = tuple(pipeline)
        self._kwargs = kwargs

    def __str__(self):
        return "<{} pipeline=({}) kwargs={}>".format(self.__class__.__name__,
                                                     ", ".join([str(x) for x in self.pipeline]), self.kwargs)

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def kwargs(self):
        return self._kwargs

    def cypher(self, s, **kwargs):
        kw = copy.deepcopy(self.kwargs.copy())
        kw.update(kwargs)
        r = copy.copy(s)
        for cypher in self.pipeline:
            r = cypher.cypher(r, **kw)
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, "cypher", s, r))
        return r

    def decypher(self, s, **kwargs):
        kw = copy.deepcopy(self.kwargs.copy())
        kw.update(kwargs)
        r = copy.copy(s)
        for cypher in reversed(self.pipeline):
            r = cypher.decypher(r, **kw)
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, "decypher", s, r))
        return r


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
