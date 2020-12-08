import sys
import unittest
import itertools

import numpy as np
import pandas as pd

from pysgrs import ciphers
from pysgrs import toolbox
from pysgrs import errors
from pysgrs import settings


class TestNGramsOnCipherKeySpace:

    factory = None
    keyspace = None
    analyzer = toolbox.NGrams(language="fr")

    paths = (settings.resources / 'texts/fr').glob("*.txt")
    plaintexts = []
    ciphertexts = []

    def load_texts(self):
        for path in self.paths:
            with path.open(encoding='utf-8') as fh:
                text = toolbox.Cleaner.strip_accents(fh.read())
                self.plaintexts.append(text)

    def generate_keyspace(self):
        for values in itertools.product(*self.keyspace.values()):
            yield {k: v for k, v in zip(self.keyspace.keys(), values)}

    def generate_ciphers(self):
        for plaintext in self.plaintexts:
            for key in self.generate_keyspace():
                cipher = self.factory(**key)
                ciphertext = cipher.encipher(plaintext)
                key.update({
                    "cipher": cipher,
                    "plaintext": plaintext,
                    "ciphertext": ciphertext
                })
                self.ciphertexts.append(key)

    def setUp(self):
        self.load_texts()
        self.generate_ciphers()


class TestNGramOnRotationCipher(TestNGramsOnCipherKeySpace, unittest.TestCase):

    factory = ciphers.RotationCipher
    keyspace = {"offset": [3, 7, 12, 16, 21, 24]}


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
