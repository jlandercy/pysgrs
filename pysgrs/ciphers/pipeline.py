import sys
import copy

from pysgrs import ciphers
from pysgrs import errors
from pysgrs.settings import settings


class PipelineCipher(ciphers.GenericCipher):

    def __init__(self, pipeline, **kwargs):
        if not all([isinstance(c, ciphers.GenericCipher) for c in pipeline]):
            raise errors.IllegalCipherParameter(
                "Pipeline must be a sequence of ciphers, received {} instead.".format(pipeline))
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

    def configuration(self):
        return {
            "pipeline": self.pipeline,
            "kwargs": self.kwargs
        }

    def encipher(self, s, **kwargs):
        kw = copy.deepcopy(self.kwargs.copy())
        kw.update(kwargs)
        r = copy.copy(s)
        for cipher in self.pipeline:
            r = cipher.encipher(r, **kw)
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, "encipher", s, r))
        return r

    def decipher(self, s, **kwargs):
        kw = copy.deepcopy(self.kwargs.copy())
        kw.update(kwargs)
        r = copy.copy(s)
        for cipher in reversed(self.pipeline):
            r = cipher.decipher(r, **kw)
        settings.logger.debug("{}.{}('{}') -> '{}'".format(self, "decipher", s, r))
        return r


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
