import sys
import unittest

from pysgrs import base
from pysgrs import settings


class Settings(unittest.TestCase):

    def test_NameSpace(self):
        self.assertIsInstance(settings.settings, settings.SimpleNamespace)

    def test_RequiredSettings(self):
        self.assertTrue({'package', 'resources', 'uuid4'}.issubset(settings.settings.__dict__))


class Alphabets(unittest.TestCase):
    pass


class Cyphers(unittest.TestCase):

    def setUp(self):
        self.identity = base.Cypher()
        self.ceasar = base.Cypher(offset=3)

    def test_IdentityCypher(self):
        self.assertEqual(self.identity.alphabet.alphabet,
                         self.identity.decypher(self.identity.cypher(self.identity.alphabet.alphabet)))

    def test_CeasarCypher(self):
        self.assertEqual(self.ceasar.alphabet.alphabet,
                         self.ceasar.decypher(self.ceasar.cypher(self.ceasar.alphabet.alphabet)))


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
