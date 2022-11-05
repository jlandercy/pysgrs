import unittest

from pysgrs import interfaces
from pysgrs import ciphers
from pysgrs import breakers
from pysgrs import scores


class GenericVigenereBreakerTest:

    _breaker = None
    _parameters_space = None
    _key_space = None


class BasicVigenereGeneticAlgorithmBreaker(GenericVigenereBreakerTest, unittest.TestCase):

    _breaker = breakers.VigenereGeneticAlgorithmBreaker()
    _text = "Je suis bien d'accord que ça prend du temps mais qu'est-ce que c'est amusant"
    _key = "EULALIE"

    def setUp(self) -> None:
        self.cipher = self._breaker.cipher_factory(key=self._key)
        self.cipher_text = self.cipher.encipher(self._text)

    def test_reversible_cipher(self):
        self.assertEqual(self._text, self.cipher.decipher(self.cipher_text))

    def test_cipher_attack(self):
        for step in self._breaker.attack(self.cipher_text, key_size=len(self._key)):
            print("{step_index}/{max_steps}\t{scoring_time:.3f}\t{min_score}\t{max_score}\t{best_key}\t{best_text}".format(**step))
