import abc
import sys
import itertools
from collections.abc import Iterable

from pysgrs.interfaces.cipher import GenericCipher
from pysgrs import errors
from pysgrs.settings import settings


class GenericGenerator(abc.ABC):
    pass


class GenericInstanceGenerator(GenericGenerator):

    @abc.abstractmethod
    def generate(self, **kwargs):
        pass


class GenericStaticGenerator(GenericGenerator):

    @staticmethod
    @abc.abstractmethod
    def generate(**kwargs):
        pass


# To deprecate:
class KeySpaceGenerator(GenericStaticGenerator):

    @staticmethod
    def coerce(**keyspace):
        def _coerce(value):
            if isinstance(value, Iterable) and not isinstance(value, str):
                return tuple(value)
            else:
                return (value,)
        return {k: _coerce(v) for k, v in keyspace.items()}

    @staticmethod
    def generate(**keyspace):
        keyspace = KeySpaceGenerator.coerce(**keyspace)
        for values in itertools.product(*keyspace.values()):
            yield {k: v for k, v in zip(keyspace.keys(), values)}


class GenericFactory(abc.ABC):

    def __init__(self, factory):
        self._factory = factory

    @property
    def factory(self):
        return self._factory

    @abc.abstractmethod
    def create(self, **kwargs):
        pass


class CipherFactory(GenericFactory, GenericInstanceGenerator):

    def __init__(self, factory, **keyspace):

        if not issubclass(factory, GenericCipher):
            raise errors.IllegalParameter("GenericFactory must be a Cipher class, received {} instead".format(type(factory)))

        super().__init__(factory)

        if not isinstance(keyspace, dict):
            raise errors.IllegalParameter("Key Space must be a dict object, received {} instead".format(type(keyspace)))

        self._keyspace = keyspace

    @property
    def keyspace(self):
        return self._keyspace

    def create(self, **kwargs):
        return self.factory(**kwargs)

    def generate(self, **keyspace):
        keyspace = keyspace or self.keyspace
        for key in KeySpaceGenerator.generate(**keyspace):
            cipher = self.create(**key)
            settings.logger.debug("Generating: {}".format(cipher))
            yield cipher


def main():

    from pysgrs.ciphers import RotationCipher

    factory = CipherFactory(RotationCipher, offset=[1, 3, 7])
    for cipher in factory.generate():
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
