import sys
import copy

from pysgrs import cyphers
from pysgrs.settings import settings


class PipelineCypher(cyphers.GenericCypher):

    def __init__(self, pipeline, **kwargs):
        assert all([isinstance(c, cyphers.GenericCypher) for c in pipeline])
        self._pipeline = tuple(pipeline)
        self._kwargs = kwargs

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def kwargs(self):
        return self._kwargs

    def cypher(self, s, **kwargs):
        kw = copy.deepcopy(self.kwargs.copy())
        kw.update(kwargs)
        for cypher in self.pipeline:
            s = cypher.cypher(s, **kw)
        return s

    def decypher(self, s, **kwargs):
        kw = copy.deepcopy(self.kwargs.copy())
        kw.update(kwargs)
        for cypher in reversed(self.pipeline):
            s = cypher.decypher(s, **kw)
        return s


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
