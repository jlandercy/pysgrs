import sys
import unittest
import itertools

import numpy as np
import pandas as pd

from pysgrs import interfaces
from pysgrs import ciphers
from pysgrs import scores
from pysgrs import toolbox
from pysgrs import errors
from pysgrs import settings


class TestNGramsOnCipherKeySpace:

    ciphers = None
    breakers = None
    analyzer = scores.MultiNGramScore(language="fr")

    paths = (settings.resources / 'texts/fr').glob("*.txt")
    plaintexts = []
    ciphertexts = []

    def load_texts(self):
        for path in self.paths:
            with path.open(encoding='utf-8') as fh:
                text = fh.read()
                plaintext = toolbox.AsciiCleaner.strip_accents(text)
                self.plaintexts.append({
                    "text": text,
                    "normalized": plaintext,
                    "score": self.analyzer.score(plaintext)
                })

    def generate_ciphers(self):
        for i, plaintext in enumerate(self.plaintexts):
            for cipher in self.ciphers.generate():
                ciphertext = cipher.encipher(plaintext["normalized"])
                obj = {
                    "configuration": cipher.configuration(),
                    "cipher": cipher,
                    "plaintext": plaintext,
                    "ciphertext": ciphertext
                }
                self.ciphertexts.append(obj)

    def apply_breaker(self):
        for ciphertext in self.ciphertexts:
            scores = []
            for cipher in self.breakers.generate():
                plaintext = cipher.decipher(ciphertext["ciphertext"])
                config = cipher.configuration()
                config["score"] = self.analyzer.score(plaintext)
                scores.append(config)
            ciphertext["breaker"] = scores

    def setUp(self):
        self.load_texts()
        self.generate_ciphers()
        self.apply_breaker()

    def test_inspect_ngrams(self):
        for results in self.ciphertexts:
            df = pd.io.json.json_normalize(results["breaker"])
            score_keys = list(df.filter(regex="score.").columns)
            df = df.sort_values(score_keys, ascending=False)
            key_keys = list(set(df.columns).difference(set(score_keys)))
            solution = df.loc[:, key_keys].iloc[0, :].to_dict()
            self.assertEqual(results["configuration"], solution)


class TestNGramOnRotationCipher(TestNGramsOnCipherKeySpace, unittest.TestCase):

    # When breakers comes after cipher, strange compiling error: AttributeError: 'CipherFactory' object has no attribute 'RotationCipher'
    breakers = interfaces.CipherFactory(ciphers.RotationCipher, offset=range(1, 26))
    ciphers = interfaces.CipherFactory(ciphers.RotationCipher, offset=[3, 7, 12, 16, 21, 24])


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
