import abc
import sys

import numpy as np

from pysgrs import scores
from pysgrs import toolbox
from pysgrs.ciphers import VigenereCipher
from pysgrs.interfaces import GenericLocalSearchBreaker, BreakerState
from pysgrs.settings import settings


class GeneticAlgorithmBreaker:

    def __init__(self, cipher, score):
        self.cipher = cipher
        self.score = score

    def guess_key_length(self, s):
        return len(self.cipher.key)

    def random_population(self, size=20):
        pass


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

    cipher = VigenereCipher(key="NOPAINNOGAIN")
    cipher_text = cipher.encipher(text)
    print(cipher_text)

    initial_score = scores.MixedNGramScore().score(cipher_text)
    print(initial_score)

    breaker = GeneticAlgorithmBreaker(cipher, scores.MixedNGramScore)
    keylength = breaker.guess_key_length(cipher_text)
    print(keylength)


if __name__ == "__main__":
    main()
