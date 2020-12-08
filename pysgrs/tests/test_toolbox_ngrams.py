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
    cipher_keyspace = None
    breaker_keyspace = None
    analyzer = toolbox.MultiNGramScore(language="fr")

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

    def generate_keyspace(self, keyspace):
        for values in itertools.product(*keyspace.values()):
            yield {k: v for k, v in zip(keyspace.keys(), values)}

    def generate_ciphers(self):
        for i, plaintext in enumerate(self.plaintexts):
            for key in self.generate_keyspace(self.cipher_keyspace):
                cipher = self.factory(**key)
                ciphertext = cipher.encipher(plaintext["normalized"])
                obj = {
                    "key": key,
                    "cipher": cipher,
                    "plaintext": plaintext,
                    "ciphertext": ciphertext
                }
                self.ciphertexts.append(obj)

    def apply_breaker(self):
        for ciphertext in self.ciphertexts:
            scores = []
            for key in self.generate_keyspace(self.breaker_keyspace):
                cipher = self.factory(**key)
                plaintext = cipher.decipher(ciphertext["ciphertext"])
                key["score"] = self.analyzer.score(plaintext)
                scores.append(key)
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
            self.assertEqual(results["key"], solution)


class TestNGramOnRotationCipher(TestNGramsOnCipherKeySpace, unittest.TestCase):

    factory = ciphers.RotationCipher
    cipher_keyspace = {"offset": [3, 7, 12, 16, 21, 24]}
    breaker_keyspace = {"offset": range(1, 26)}


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
