import abc
import sys

import numpy as np

from pysgrs import scores
from pysgrs import toolbox
from pysgrs.alphabets import BasicAlphabet
from pysgrs.ciphers import VigenereCipher
from pysgrs.interfaces import GenericLocalSearchBreaker, BreakerState
from pysgrs.settings import settings


class GeneticAlgorithmBreaker:

    def __init__(self, cipher, score, key_size):
        self.cipher = cipher
        self.alphabet = BasicAlphabet()
        self.score = score
        self.key_size = key_size

    def guess_key_length(self, s):
        return self.key_size

    def random_population(self, population_size=20):
        return ["".join(np.random.choice(list(self.alphabet.symbols), size=self.key_size)) for i in range(population_size)]

    def make_pairs(self, group):
        group = np.array(group)
        np.random.shuffle(group)
        n = group.size//2
        return [pair for pair in zip(group[:n], group[n:])]

    def random_index(self):
        return np.random.choice(range(self.key_size))

    def mutate(self, old_1, old_2):
        i, j = self.random_index(), self.random_index()
        i, j = min(i, j), max(i, j)
        new_1 = list(old_1)
        new_2 = list(old_2)
        new_1[i] = old_2[j]
        new_1[j] = old_2[i]
        new_2[i] = old_1[j]
        new_2[j] = old_1[i]
        return "".join(new_1), "".join(new_2)

    def crossing(self, old_1, old_2, threshold=0.8):
        index = self.random_index()
        new_1 = old_1[:index] + old_2[index:]
        new_2 = old_2[:index] + old_1[index:]
        if np.random.rand() >= threshold:
            new_1, new_2 = self.mutate(new_1, new_2)
        return new_1, new_2

    def group_crossing(self, group):
        new_group = []
        for pair in self.make_pairs(group):
            new_pair = self.crossing(*pair)
            new_group.extend(new_pair)
        return new_group

    def score_group(self, text, group):
        return [self.score.score(VigenereCipher(key=key).decipher(text)) for key in group]

    def attack(self, text, population_size=20, generation_count=30):

        # Create random population:
        initial_group = self.random_population(population_size=population_size)
        initial_scores = self.score_group(text, initial_group)
        #print(initial_group, initial_scores)

        for i in range(generation_count):

            # Create a new population by crossing and mutating:
            new_group = self.group_crossing(initial_group)
            new_scores = self.score_group(text, new_group)
            #print(new_group, new_scores)

            # Merge groups:
            group = initial_group + new_group
            group_scores = initial_scores + new_scores
            index = np.argsort(group_scores)

            # Keep best representative:
            initial_group = list(np.array(group)[index][population_size:])
            initial_scores = list(np.array(group_scores)[index][population_size:])

            print(i, np.min(group_scores), np.max(group_scores), np.min(initial_scores), np.max(initial_scores), initial_group[-1])

        return initial_group[-1]


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
    text = toolbox.AsciiCleaner.strip_accents(text)
    print(text)

    target_score = scores.MixedNGramScore().score(text)
    print(target_score)

    key = "RANDOMACCESSMEMORY"
    cipher = VigenereCipher(key=key)
    cipher_text = cipher.encipher(text)
    print(cipher_text)

    initial_score = scores.MixedNGramScore().score(cipher_text)
    print(initial_score)

    breaker = GeneticAlgorithmBreaker(VigenereCipher, scores.MixedNGramScore(), key_size=len(key))
    new_key = breaker.attack(cipher_text, population_size=100, generation_count=100)

    new_cipher = VigenereCipher(key=new_key)
    decipher_text = new_cipher.decipher(cipher_text)
    print(decipher_text)


if __name__ == "__main__":
    main()
