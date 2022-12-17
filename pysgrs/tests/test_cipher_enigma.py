import unittest

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

    def test_encrypt(self):
        message = 'Hello World'
        secret = self.engine.encipher(message)
        self.assertEqual(secret, 'Qgqop Vyzxp')
