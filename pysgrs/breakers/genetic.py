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
        return BreakerState(population=self._random_population(), counter=0, trial_counter=0)

    def _convert_likelihood_to_probability(self, likelihood):
        p = 1.0/likelihood**2
        return p/np.sum(p)

    def _crossover(self, x, y, min_length=5, max_length=8):
        # PMX
        length = np.random.randint(min_length, max_length)
        index = np.random.randint(0, x.size - length)
        offspring = x.copy()
        own_gene = x[index:index+length+1]
        new_gene = y[index:index+length+1]
        conflict = set(new_gene).difference(set(own_gene).intersection(new_gene))
        offspring[index:index+length+1] = new_gene
        missing = set(x).difference(offspring)
        for (outsider, insider) in zip(conflict, missing):
            idx = np.where(x == outsider)[0][0]
            offspring[idx] = insider
        return offspring

    def _mutate(self, x):
        idx = np.random.choice(x.size, size=2, replace=False)
        x[idx] = x[np.flip(idx)]
        return x

    def _july_do_the_thing(self, mutation_probability=0.001):
        # Select parents:
        index = np.random.choice(self.current_state.population.shape[0],
                                 size=2, replace=False, p=self.current_state.probability)
        parents = self.current_state.population[index, :]
        # Perform cross-over:
        offspring = self._crossover(*parents)
        # Mutation:
        if np.random.random() < mutation_probability:
            offspring = self._mutate(offspring)
        return offspring

    def _next_state(self, **kwargs):
        self._current_state.counter += 1
        next_state = self.current_state.copy()
        next_state.population = []
        for k in range(self.current_state.population.shape[0]):
            next_state.population.append(self._july_do_the_thing())
        next_state.population = np.array(next_state.population)
        return next_state

    def _score_state(self, state, text):
        state.score = []
        for individual in state.population:
            cipher = PermutationCipher(permutation=individual)
            state.score.append(self.score.score(cipher.decipher(text)))
        state.score = np.array(state.score)
        state.probability = self._convert_likelihood_to_probability(state.score)
        state.fittest = np.argmax(state.score)
        return state

    def attack(self, text, max_trials=50, **kwargs):

        self._current_state = self._score_state(self._initial_state(), text)

        while True:

            yield self.current_state

            next_state = self._score_state(self._next_state(**kwargs), text)

            if np.max(next_state.score) > np.max(self.current_state.score):
                self._current_state = next_state
                self._current_state.trial_counter = 0
            else:
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

    for state in GeneticAlgorithmBreaker(s).attack(c):
        #print("{score:.3f}/{solution_score:.3f} {correct_digit:}".format(
        #      solution_score=s0, correct_digit=sum(p == state.population[state.fittest,:]), **state.to_dict()))
        print(state.counter, state.trial_counter, max(state.score), state.probability, state.score, state.fittest)

    Cs = PermutationCipher(state.population[0,:])

    print(t)
    print(c)
    print(Cs.decipher(c))
    sys.exit(0)


if __name__ == "__main__":
    main()
