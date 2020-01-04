import sys
import unittest

from pysgrs import settings


class Settings(unittest.TestCase):

    def test_NameSpace(self):
        self.assertIsInstance(settings.settings, settings.SimpleNamespace)

    def test_RequiredSettings(self):
        self.assertTrue({'package', 'resources', 'uuid4'}.issubset(settings.settings.__dict__))


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
