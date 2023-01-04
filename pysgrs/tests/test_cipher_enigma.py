import logging
import unittest
import copy

from pysgrs.ciphers.enigma import *


logger = logging.getLogger(__name__)


class TestSimpleEnigmaCipher(unittest.TestCase):

    def setUp(self):
        self.engine = Enigma

    def test_cipher(self):
        print(self.engine)
        text = 'Hello World'
        cipher_text = self.engine.encipher(text)
        print(self.engine)
        self.assertEqual(cipher_text, 'Qgqop Vyzxp')

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
        self.engine = Engine(
            rotors=(IM3M4_R1, IM3M4_R2, IM3M4_R3),
            reflector=IM3M4_UKW_B,
            rotor_states='EUL',
            plugs='BQ CR DI EJ KW MT OS PX UZ GH'
        )

    def generate(self, callback):
        for index, (text, cipher_text) in enumerate(zip(self.texts, self.cipher_texts)):
            logger.info("Text: %s, Cipher: %s" % (text, cipher_text))
            self.engine.reset()
            logger.info("Engine: %s " % self.engine)
            result = callback(self.engine, locals())
            logger.info("Result: %s" % result)
            logger.info("Engine: %s " % self.engine)
            yield {
                "index": index,
                "engine": self.engine,
                "text": text,
                "cipher_text": cipher_text,
                "result": result
            }

    def test_cipher(self):

        def callback(engine, context):
            return {"cipher_text": engine.encipher(context["text"])}

        for sample in self.generate(callback):
            logger.info(sample)

    def test_reflector_reflectivity(self):
        reflector = self.engine.reflector_
        logger.info("Reflector: %s" % reflector)
        for symbol in self.engine.alphabet.symbols:
            encoded = reflector.encipher(symbol)
            decoded = reflector.decipher(encoded)
            self.assertEqual(symbol, decoded)

    def test_rotor_reflectivity(self):
        for rotor in self.engine.rotors_:
            logger.info("Rotor: %s" % rotor)
            for symbol in self.engine.alphabet.symbols:
                encoded = rotor.encipher(symbol)
                decoded = rotor.decipher(encoded)
                self.assertEqual(symbol, decoded)

    def test_rotor_mapping(self):
        for rotor in self.engine.rotors_:
            logger.info("Rotor: %s" % rotor)
            print(rotor.direct_mapping)
            print(rotor.inverse_mapping)

    def test_rotor_reflectivity_superclass(self):
        for rotor in self.engine.rotors_:
            logger.info("Rotor: %s" % rotor)
            for symbol in self.engine.alphabet.symbols:
                encoded = super(Wheel, rotor).encipher(symbol)
                decoded = super(Wheel, rotor).decipher(encoded)
                self.assertEqual(symbol, decoded)

    def test_cipher_illegal_symbol(self):
        for text, cipher_text in zip(self.texts, self.cipher_texts):
            self.engine.reset()
            print(self.engine)
            check = self.engine.encipher(text)
            print(self.engine)
            for c1, c2 in zip(check, text):
                if c2 in self.engine.alphabet.symbols:
                    self.assertNotEqual(c1, c2)

