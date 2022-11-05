import itertools

import numpy as np

from pysgrs.alphabets.basic import BasicAlphabet
from pysgrs.interfaces.space import GenericSpace


class ParameterSpace(GenericSpace):

    def __init__(self, **parameters):
        self._parameters = parameters

    @property
    def parameters(self):
        return self._parameters

    def generate(self, mode="dict"):
        for parameter in itertools.product(*[value for value in self.parameters.values()]):
            if mode == "dict":
                yield {key: value for key, value in zip(self.parameters.keys(), parameter)}
            else:
                yield parameter

    def sample(self, size=1):
        pass


class KeySpace(GenericSpace):

    def __init__(self, alphabet, min_key_size=10, max_key_size=None):

        self._alphabet = alphabet

        if max_key_size is None:
            max_key_size = min_key_size

        self._min_key_size = min_key_size
        self._max_key_size = max_key_size

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def min_key_size(self):
        return self._min_key_size

    @property
    def max_key_size(self):
        return self._max_key_size

    @property
    def key_sizes(self):
        return np.arange(self.min_key_size, self.max_key_size + 1)

    @property
    def key_space_sizes(self):
        return np.power(np.full(self.key_sizes.shape, fill_value=1.)*self.alphabet.size, self.key_sizes)

    def sample_key_size(self, size=1):
        return np.random.choice(self.key_sizes, size=size, p=self.key_space_sizes/self.size())

    def generate(self, mode="dict", join=True):
        for key_size in self.key_sizes:
            for key in itertools.product(self.alphabet.symbols, repeat=key_size):
                if join:
                    key = "".join(key)
                if mode == "dict":
                    yield {"key_size": key_size, "key": key}
                else:
                    yield key

    def sample(self, size=1, weights=None):
        key_sizes = self.sample_key_size(size=size)
        keys = []
        for key_size in key_sizes:
            key = np.random.choice(list(self.alphabet.symbols), size=key_size, p=weights)
            keys.append("".join(key))
        return keys

    def size(self):
        return np.sum(self.key_space_sizes)


basic_space_10 = KeySpace(
    alphabet=BasicAlphabet(),
    min_key_size=10,
    max_key_size=10
)
