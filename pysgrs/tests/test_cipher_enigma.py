import unittest
import copy

from pysgrs.ciphers.enigma import *


class TestSimpleEnigmaCipher(unittest.TestCase):

    def setUp(self):
        self.engine = Enigma

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
        print(self.engine)
        self.assertEqual(decipher_text, text)


class TestEnigmaCipher(unittest.TestCase):

    texts = [
        "il faut laisser le temps au temps"
    ]
    cipher_texts = [
        "xn czgk wsbpkvb no afklo un pirzp"
    ]

    def setUp(self):
        self.engine = Enigma(
            IM3M4_UKW_B,
            IM3M4_R1,
            IM3M4_R2,
            IM3M4_R3,
            key='EUL',
            plugs='BQ CR DI EJ KW MT OS PX UZ GH'
        )

    def test_cipher(self):
        for text, cipher_text in zip(self.texts, self.cipher_texts):
            engine = copy.deepcopy(self.engine)
            print(engine)
            check = engine.encipher(text)
            print(engine)
            self.assertEqual(check, cipher_text)

