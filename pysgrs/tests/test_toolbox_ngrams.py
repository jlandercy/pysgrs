import sys
import unittest

import numpy as np

from pysgrs import ciphers
from pysgrs import toolbox
from pysgrs import errors
from pysgrs import settings


class test_ngrams_CaesarCipher(unittest.TestCase):

    cipher = ciphers.CaesarCipher()
    paths = (settings.resources / 'texts/fr').glob("*.txt")
    plaintexts = []
    ciphertexts = []

    def setUp(self):
        for path in self.paths:
            with path.open(encoding='utf-8') as fh:
                text = toolbox.Cleaner.strip_accents(fh.read())
                self.plaintexts.append(text)
            cipher = self.cipher.encipher(text)
            self.ciphertexts.append(cipher)

    def test_me(self):
        pass


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
