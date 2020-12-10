import sys
import unittest

import pandas as pd

from pysgrs import interfaces
from pysgrs import ciphers
from pysgrs import toolbox
from pysgrs import errors
from pysgrs import settings


class TestBruteForceBreaker:

    ciphers = None
    breaker = None

    paths = (settings.resources / 'texts/fr').glob("*.txt")
    plaintexts = []
    ciphertexts = []
    results = []

    def load_texts(self):
        for path in self.paths:
            with path.open(encoding='utf-8') as fh:
                text = fh.read()
                plaintext = toolbox.AsciiCleaner.strip_accents(text)
                self.plaintexts.append({
                    "text": text,
                    "normalized": plaintext,
                    "score": self.breaker.score.score(plaintext)
                })

    def generate_ciphertexts(self):
        for plaintext in self.plaintexts:
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
            results = []
            for result in self.breaker.attack(ciphertext["ciphertext"]):
                results.append(result)
            self.results.append(results)

    def setUp(self):
        self.load_texts()
        self.generate_ciphertexts()
        self.apply_breaker()

    def test_complete_attack_results(self):
        for (solution, results) in zip(self.ciphertexts, self.results):
            df = pd.DataFrame(results).sort_values("score", ascending=False).reset_index()
            optimum = df.loc[0, "configuration"]
            self.assertEqual(solution["configuration"], optimum)


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
