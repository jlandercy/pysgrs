import unittest

from pysgrs import interfaces
from pysgrs import ciphers
from pysgrs import breakers
from pysgrs import scores


class GenericVigenereBreaker:

    _parameters_space = None
    _key_space = None


class LightWeightVigenereBreaker(GenericVigenereBreaker, unittest.TestCase):

    def test_dummy(self):
        pass
