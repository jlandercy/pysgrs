import sys

import numpy as np
import pandas as pd

from pysgrs.interfaces import GenericBreaker
from pysgrs.settings import settings


class BruteForceBreaker(GenericBreaker):

    def attack(self, ciphertext, **kwargs):
        for cipher in self.factory.generate(**kwargs):
            trialtext = cipher.decipher(ciphertext)
            score = self.score.score(trialtext)
            yield {
                "cipher": cipher,
                "configuration": cipher.configuration(),
                "score": score
            }

    def analyze(self, text, **kwargs):
        results = [result for result in self.attack(text, **kwargs)]
        return pd.DataFrame(results).sort_values("score", ascending=False).reset_index()

    def guess(self, text, **kwargs):
        return self.analyze(text, **kwargs).loc[0, "configuration"]


def main():

    from pysgrs import interfaces, ciphers, scores, breakers

    t = "Attention derrière toi, il y a un train qui en cache un autre!"
    C = ciphers.RotationCipher(offset=17)
    c = C.encipher(t)
    print(t)
    print(C)
    print(c)

    BF = breakers.BruteForceBreaker(
        interfaces.CipherFactory(ciphers.RotationCipher, offset=range(0, 27)),
        scores.MultiNGramScore().ngrams[2]
    )

    for result in BF.attack(c):
        print(result["configuration"], result["score"]["value"])

    sys.exit(0)


if __name__ == "__main__":
    main()
