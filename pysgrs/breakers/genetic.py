import abc
import sys

import numpy as np

from pysgrs.ciphers import PermutationCipher
from pysgrs.interfaces import GenericLocalSearchBreaker, BreakerState
from pysgrs.settings import settings


class GeneticAlgorithmBreaker(GenericLocalSearchBreaker):

    def _random_population(self, size=26, population_size=10):
        population = np.array([np.random.permutation(size) for i in range(population_size)])
        return population

    def _initial_state(self, **kwargs):
        return BreakerState(population=self._random_population(), counter=0)

    def _july_do_the_thing(self):
        parents = np.random.choice(self.current_state.population.shape[0],
                                   size=2, replace=False)#, p=self.current_state.score)
        crosspoint = np.random.randint(self.current_state.population.shape[1])
        offspring = self.current_state.population[parents[0], :]
        offspring[crosspoint:] = self.current_state.population[parents[1], crosspoint:]
        print(offspring)
        return offspring

    def _next_state(self, **kwargs):
        next_population = []
        for k in range(self.current_state.population.shape[0]):
            next_population.append(self._july_do_the_thing())
        return BreakerState(population=next_population)

    def _score_state(self, state, text):
        state.score = []
        for individual in state.population:
            cipher = PermutationCipher(permutation=individual)
            state.score.append(self.score.score(cipher.decipher(text)))
        print(state.score)
        return state

    def attack(self, text, max_trials=1000, **kwargs):
        self._current_state = self._score_state(self._initial_state(), text)
        while True:

            yield self.current_state

            next_state = self._score_state(self._next_state(**kwargs), text)

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

    for state in GeneticAlgorithmBreaker(s).attack(c):
        #print("{counter:}/{trial_counter:} {score:.3f}/{solution_score:.3f} {correct_digit:}".format(
        #    solution_score=s0, correct_digit=sum(p == state.permutation), **state.to_dict()))
        print(state)

    Cs = PermutationCipher(state.population[0,:])

    print(t)
    print(c)
    print(Cs.decipher(c))
    sys.exit(0)


if __name__ == "__main__":
    main()
