import abc
import sys

import numpy as np

from pysgrs.ciphers import PermutationCipher
from pysgrs.interfaces import GenericLocalSearchBreaker, BreakerState
from pysgrs.settings import settings


class StochasticHillClimbingBreaker(GenericLocalSearchBreaker):

    def _initial_state(self, size=26, **kwargs):
        return BreakerState(permutation=np.random.permutation(size), counter=0, trial_counter=0)

    def _next_state(self, **kwargs):
        self._current_state.counter += 1
        next_state = self.current_state.copy()
        idx = np.random.choice(next_state.permutation.size, size=2, replace=False)
        next_state.permutation[idx] = next_state.permutation[np.flip(idx)]
        return next_state

    def _score_state(self, state, text):
        cipher = PermutationCipher(permutation=state.permutation)
        state.score = self.score.score(cipher.decipher(text))
        return state

    def attack(self, text, max_trials=1000, **kwargs):

        # Create and score Initial State:
        self._current_state = self._score_state(self._initial_state(**kwargs), text)

        # Perform Steepest Ascent:
        while True:

            # Yield Current State:
            yield self.current_state

            # Sample and score Next State:
            next_state = self._score_state(self._next_state(**kwargs), text)

            # Is the next state better than the current?
            if next_state.score > self.current_state.score:
                # Then go for it!
                self._current_state = next_state
                self._current_state.trial_counter = 0
            else:
                # Look a bit further to see if there is something else:
                self._current_state.trial_counter += 1
                if self.current_state.trial_counter > max_trials:
                    break

    def analyze(self, text, **kwargs):
        pass

    def guess(self, text, **kwargs):
        pass


def main():
    from pysgrs import scores
    from pysgrs import toolbox

    t = """Bonjour tout le monde, on essaye des trucs, on teste, mais c'est pas absolu comme méthode...
    Il sera sans doute nécessaire de s'appliquer d'avantage pour mieux comprendre les tenants et aboutissants
    d'une telle méthodologie. En ajoutant du texte on parvient à améliorer le score et donc le critère de
    convergence semble plus efficace, même si ça reste une illusion de pouvoir explorer l'esapce des états de
    manière exhaustive. Mais bon, en rejouant plusieurs fois l'algorithme on parvient à trouver vingt-deux
    des vingt-six caractères recherchés en moins de dix mille itérations et ça c'est déjà quelque chose
    de positif et encourageant. Il est a noter que la taille, mais également le contenu du texte ont de
    de l'importance. A cela s'ajoute également que la solution exacte n'est pas forcément celle qui possède
    le plus haut score en terme de maximum de vraissemblance des digrammes."""

    t = toolbox.AsciiCleaner.strip_accents(t)

    p = np.random.permutation(26)
    C = PermutationCipher(p)
    c = C.encipher(t)

    s = scores.NGramScore(order=3)
    s0 = s.score(t)

    for state in StochasticHillClimbingBreaker(s).attack(c):
        print("{counter:}/{trial_counter:} {score:.3f}/{solution_score:.3f} {correct_digit:}".format(
            solution_score=s0, correct_digit=sum(p == state.permutation), **state.to_dict()))

    Cs = PermutationCipher(state.permutation)

    print(t)
    print(c)
    print(Cs.decipher(c))
    sys.exit(0)


if __name__ == "__main__":
    main()
