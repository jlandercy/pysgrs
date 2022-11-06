import unittest

from pysgrs import interfaces
from pysgrs import ciphers
from pysgrs import breakers
from pysgrs import scores
from pysgrs import toolbox


class GenericVigenereBreakerTest:

    _breaker = None
    _parameters_space = None
    _key_space = None


class BasicVigenereGeneticAlgorithmBreaker(GenericVigenereBreakerTest, unittest.TestCase):

    _breaker = breakers.VigenereGeneticAlgorithmBreaker()
    _text = """
    Bonjour tout le monde, on essaye des trucs, on teste, mais c'est pas absolu comme méthode...
    Il sera sans doute nécessaire de s'appliquer d'avantage pour mieux comprendre les tenants et aboutissants
    d'une telle méthodologie. En ajoutant du texte on parvient à améliorer le score et donc le critère de
    convergence semble plus efficace, même si ça reste une illusion de pouvoir explorer l'esapce des états de
    manière exhaustive. Mais bon, en rejouant plusieurs fois l'algorithme on parvient à trouver vingt-deux
    des vingt-six caractères recherchés en moins de dix mille itérations et ça c'est déjà quelque chose
    de positif et encourageant. Il est a noter que la taille, mais également le contenu du texte ont de
    de l'importance. A cela s'ajoute également que la solution exacte n'est pas forcément celle qui possède
    le plus haut score en terme de maximum de vraissemblance des n-grammes.
    """
    _key = "SECRETTOKEN"

    def setUp(self) -> None:
        self.cipher = self._breaker.cipher_factory(key=self._key)
        self.cipher_text = self.cipher.encipher(toolbox.AsciiCleaner.strip_accents(self._text))

    def test_reversible_cipher(self):
        self.assertEqual(self._text, self.cipher.decipher(self.cipher_text))

    def test_cipher_attack(self):
        for step in self._breaker.attack(self.cipher_text, key_size=len(self._key)):
            step["best_text_short"] = step["best_text"][:64].replace("\n", "")
            print("{step_index}/{max_steps}\t{scoring_time:.3f}\t{population_size}\t{key_size}\t{min_score}\t{max_score}\t{best_key}\t{best_text_short}".format(**step))

    def test_original_version(self):
        for step in breakers.VigenereGeneticAlgorithmBreaker_v1(
            score=scores.mixed_ngrams_fr
        ).attack(
            self.cipher_text, key_size=len(self._key),
            population_size=100, generation_count=50,
            threshold=0.2, seed=123,
            exact_key=self._key
        ):
            pass
