import abc
import sys

import numpy as np
import pandas as pd
from scipy.spatial import distance

from pysgrs import scores
from pysgrs.toolbox import AsciiCleaner, Shaper, FrequencyAnalyzer
from pysgrs.alphabets import BasicAlphabet
from pysgrs.interfaces import GenericLocalSearchBreaker, BreakerState
from pysgrs.ciphers import VigenereCipher
from pysgrs.settings import settings


class VigenereGeneticAlgorithmBreaker(GenericLocalSearchBreaker):

    def __init__(self, score, alphabet=BasicAlphabet(), language="fr"):
        super().__init__(score)
        self.factory = VigenereCipher
        self.alphabet = alphabet
        self.language = language

    def _initial_state(self, **kwargs):
        pass

    def _next_state(self, **kwargs):
        pass

    def _score_state(self, text, **kwargs):
        pass

    def analyze(self, text, **kwargs):
        pass

    def guess(self, text, **kwargs):
        pass

    def guess_key_sizes(self, text, min_key_size=1, max_key_size=48, normalize=True, order_by="min"):
        if normalize:
            text = AsciiCleaner.normalize(text)
        coincidences = FrequencyAnalyzer.keysize_coincidences(text, min_key_size=min_key_size, max_key_size=max_key_size)
        guesses = coincidences.groupby("key_size")["coincidence"].agg(["min", "mean", "median", "max"]).sort_values(order_by, ascending=False)
        guesses.columns = guesses.columns.map(lambda x: "coincidence_" + x)
        return guesses

    def random_population(self, key_size, population_size=20):
        return ["".join(np.random.choice(list(self.alphabet.symbols), size=key_size)) for i in range(population_size)]

    def make_pairs(self, group):
        group = np.array(group)
        np.random.shuffle(group)
        n = group.size//2
        return [pair for pair in zip(group[:n], group[n:])]

    def random_index(self, key_size):
        return np.random.choice(range(key_size))

    def mutate(self, old_1, old_2):
        i, j = self.random_index(len(old_1)), self.random_index(len(old_2))
        i, j = min(i, j), max(i, j)
        new_1 = list(old_1)
        new_2 = list(old_2)
        new_1[i] = old_2[j]
        new_1[j] = old_2[i]
        new_2[i] = old_1[j]
        new_2[j] = old_1[i]
        return "".join(new_1), "".join(new_2)

    def crossing(self, old_1, old_2, mutation_threshold=0.8):
        index = self.random_index(len(old_1))
        new_1 = old_1[:index] + old_2[index:]
        new_2 = old_2[:index] + old_1[index:]
        if np.random.rand() >= mutation_threshold:
            new_1, new_2 = self.mutate(new_1, new_2)
        return new_1, new_2

    def group_crossing(self, group, mutation_threshold=0.8):
        new_group = []
        for pair in self.make_pairs(group):
            new_pair = self.crossing(*pair, mutation_threshold=mutation_threshold)
            new_group.extend(new_pair)
        return new_group

    def score_group(self, text, group):
        return [self.score.score(VigenereCipher(key=key).decipher(text)) for key in group]

    def attack_with_key_size_guess(self, text, min_key_size=10, max_key_size=48, order_by="min", max_guess=5, **kwargs):
        key_sizes = self.guess_key_sizes(text, min_key_size=min_key_size, max_key_size=max_key_size, order_by=order_by).reset_index()
        print(key_sizes)
        for key_size in key_sizes.iloc[:max_guess].to_dict(orient='records'):
            for record in self.attack(text, key_size=key_size["key_size"], **kwargs):
                record.update(key_size)
                yield record

    def attack(self, text, key_size=None, population_size=20, generation_count=30, mutation_threshold=0.8):

        # Create random population:
        initial_group = self.random_population(key_size, population_size=population_size)
        initial_scores = self.score_group(text, initial_group)

        for i in range(generation_count):

            # Create a new population by crossing and mutating:
            new_group = self.group_crossing(initial_group, mutation_threshold=mutation_threshold)
            new_scores = self.score_group(text, new_group)

            # Merge groups:
            group = initial_group + new_group
            group_scores = initial_scores + new_scores
            index = np.argsort(group_scores)

            # Keep best representative:
            initial_group = list(np.array(group)[index][population_size:])
            initial_scores = list(np.array(group_scores)[index][population_size:])

            generation = {
                "generation": i+1,
                "generation_count": generation_count,
                "mutation_threshold": mutation_threshold,
                "key_size": key_size,
                "population_size": population_size,
                "global_min": np.min(group_scores),
                "global_max": np.max(group_scores),
                "selection_min": np.min(initial_scores),
                "selection_max": np.max(initial_scores),
                "best_individual": initial_group[-1],
                "group": group,
            }
            print("{generation}/{generation_count:}\t{key_size:}\t{mutation_threshold:}\t{selection_min:.3f}\t{selection_max:.3f}\t{best_individual:}".format(**generation))
            yield generation


def main():

    text = """
    Bonjour tout le monde, on essaye des trucs, on teste, mais c'est pas absolu comme méthode...
    Il sera sans doute nécessaire de s'appliquer d'avantage pour mieux comprendre les tenants et aboutissants
    d'une telle méthodologie. En ajoutant du texte on parvient à améliorer le score et donc le critère de
    convergence semble plus efficace, même si ça reste une illusion de pouvoir explorer l'esapce des états de
    manière exhaustive. Mais bon, en rejouant plusieurs fois l'algorithme on parvient à trouver vingt-deux
    des vingt-six caractères recherchés en moins de dix mille itérations et ça c'est déjà quelque chose
    de positif et encourageant. Il est a noter que la taille, mais également le contenu du texte ont de
    de l'importance. A cela s'ajoute également que la solution exacte n'est pas forcément celle qui possède
    le plus haut score en terme de maximum de vraissemblance des digrammes.
    """
    text = AsciiCleaner.strip_accents(text)
    print(text)

    target_score = scores.MixedNGramScore().score(text)
    print(target_score)

    key = "GENETICALGORITHM"
    print(len(key))
    cipher = VigenereCipher(key=key)
    cipher_text = cipher.encipher(text)
    print(cipher_text)

    initial_score = scores.MixedNGramScore().score(cipher_text)
    print(initial_score)

    breaker = VigenereGeneticAlgorithmBreaker(scores.MixedNGramScore())

    generations = list(breaker.attack_with_key_size_guess(cipher_text, min_key_size=5, max_key_size=20, order_by="mean", population_size=250, generation_count=30, mutation_threshold=0.50))

    df = pd.DataFrame(generations)
    df.to_excel("breaker_ga.xlsx")
    print(df)


if __name__ == "__main__":
    main()
