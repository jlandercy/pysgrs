import sys

import numpy as np

from pysgrs.ciphers import PermutationCipher
from pysgrs.interfaces import GenericBreaker
from pysgrs.settings import settings


class StochasticHillClimbingBreaker(GenericBreaker):

    def _inital_state(self, size=26):
        return np.random.permutation(size)

    def _next_state(self, current_state, size=26):
        idx = np.random.choice(size, size=2, replace=False)
        next_state = current_state.copy()
        next_state[idx] = next_state[list(reversed(idx))]
        return next_state

    def _scorer(self, text, state):
        return self.score.score(PermutationCipher(state).decipher(text))

    def attack(self, text, max_trials=1000, **kwargs):

        # Inital State:
        counter = 0
        trial_counter = 0
        current_state = self._inital_state()
        while True:

            # Score current state:
            current_score = self._scorer(text, current_state)
            yield {
                "counter": counter,
                "trial_counter": trial_counter,
                "current_state": current_state,
                "current_score": current_score
            }

            # Sample and score new state:
            next_state = self._next_state(current_state)
            next_score = self._scorer(text, next_state)
            counter += 1

            # Decide what to do?
            if next_score > current_score:
                trial_counter = 0
                current_state = next_state
            else:
                trial_counter += 1
                if trial_counter > max_trials:
                    break

    def analyze(self, text, **kwargs):
        pass

    def guess(self, text, **kwargs):
        pass


def main():
    from pysgrs import scores

    t = """Bonjour tout le monde, on essaye des trucs, on teste, mais c'est pas absolu comme méthode...
    Il sera sans doute nécessaire de s'appliquer d'avantage pour mieux comprendre les tenants et aboutissant
    d'une telle méthodologie. En ajoutant du texte on parvient à améliorer le score et donc le critère de
    ceovergence semble plus efficace, même si ça reste une illusion de pouvoir explore l'esapce des états de
    manière exhaustive"""

    p = np.random.permutation(26)
    C = PermutationCipher(p)
    c = C.encipher(t)

    s = scores.NGramScore(order=2)
    s0 = s.score(t)

    for state in StochasticHillClimbingBreaker(s).attack(c):
        print("{counter:}, {trial_counter:}: {current_score:.3f} ({real_score:.3f}): {correct_digit:}".format(
            **state, real_score=s0, correct_digit=sum(p == state["current_state"])))

    Cs = PermutationCipher(state["current_state"])

    print(t)
    print(c)
    print(Cs.decipher(c))
    sys.exit(0)


if __name__ == "__main__":
    main()
