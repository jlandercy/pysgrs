import unittest
import copy

from pysgrs.ciphers.enigma import *


class TestEnigmaCipher(unittest.TestCase):

    def setUp(self):
        self.engine = Enigma(
            ROTOR_Reflector_A,
            ROTOR_I,
            ROTOR_II,
            ROTOR_III,
            key='ABC',
            plugs='AV BS CG DL FU HZ IN KM OW RX'
        )

    def test_cipher(self):
        print(self.engine)
        text = 'Hello World'
        cipher_text = self.engine.encipher(text)
        self.assertEqual(cipher_text, 'Qgqop Vyzxp')
        print(self.engine)

    def test_cipher_decipher(self):
        clone = copy.deepcopy(self.engine)
        print(self.engine)
        text = 'Hello World'
        cipher_text = self.engine.encipher(text)
        decipher_text = clone.encipher(cipher_text)
        self.assertEqual(cipher_text, 'Qgqop Vyzxp')
        self.assertEqual(decipher_text, text)
        print(self.engine)
