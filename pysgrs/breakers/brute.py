import sys

import numpy as np

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
                "score": {
                    "function": self.score,
                    "value": score
                },
                "texts": {
                    "ciphertext": ciphertext,
                    "trialtext": trialtext
                }
            }

    def guess(self, text, **kwargs):
        max_score = -np.inf


def main():

    from pysgrs import interfaces, ciphers, scores, breakers

    BF = breakers.BruteForceBreaker(
        interfaces.CipherFactory(ciphers.RotationCipher, offset=range(0, 27)),
        scores.MultiNGramScore().ngrams[2]
    )

    for result in BF.attack("Attention derrière toi, il y a un train qui en cache un autre!"):
        print(result["configuration"], result["score"]["value"])

    sys.exit(0)


if __name__ == "__main__":
    main()
