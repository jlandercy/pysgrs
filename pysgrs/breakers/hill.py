import sys

import numpy as np

from pysgrs.ciphers import PermutationCipher
from pysgrs.interfaces import GenericBreaker
from pysgrs.settings import settings


class HillClimbingBreaker(GenericBreaker):

    def _inital_state(self, size=26):
        return np.random.permutation(size)

    def _next_state(self, current_state, size=26):
        idx = np.random.choice(size, size=2, replace=False)
        next_state = current_state.copy()
        next_state[idx] = next_state[list(reversed(idx))]
        return next_state

    def _scorer(self, text, state):
        return self.score.score(PermutationCipher(state).decipher(text))

    def attack(self, text, **kwargs):
        miss_counter = 0
        current_state = self._inital_state()
        while True:
            current_score = self._scorer(text, current_state)
            yield current_score, current_state
            next_state = self._next_state(current_state)
            next_score = self._scorer(text, next_state)
            if next_score > current_score:
                miss_counter = 0
                current_state = next_state
            else:
                miss_counter += 1
            if miss_counter > 1000:
                break

    def analyze(self, text, **kwargs):
        pass

    def guess(self, text, **kwargs):
        pass


def main():
    from pysgrs import scores
    p = np.random.permutation(26)
    C = PermutationCipher(p)
    c = C.encipher("Bonjour tout le monde, on essaye des trucs, on teste...")
    print(c)
    for k, v in HillClimbingBreaker(scores.NGramScore(order=3)).attack(c):
        print(k, p == v,  p, v)
    sys.exit(0)


if __name__ == "__main__":
    main()
