import sys
import unittest

from pysgrs import errors
from pysgrs import settings


class TestStreamCipher:

    cipher = None
    plaintexts = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBA",
        "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
        "WALTZBADNYMPHFORQUICKJIGSVEX",
        "JIVEDFOXNYMPHGRABSQUICKWALTZ",
        "GLIBJOCKSQUIZNYMPHTOVEXDWARF",
        "SPHINXOFBLACKQUARTZJUDGEMYVOW",
        "HOWVEXINGLYQUICKDAFTZEBRASJUMP",
        "THEFIVEBOXINGWIZARDSJUMPQUICKLY",
        "JACKDAWSLOVEMYBIGSPHINXOFQUARTZ",
        "PACKMYBOXWITHFIVEDOZENLIQUORJUGS",
        "Live as if you were to die tomorrow. Learn as if you were to live forever.",
        "Be who you are and say what you feel, because those who mind don’t matter and those who matter don’t mind.",
        "If you cannot do great things, do small things in a great way.",
        "Wise men speak because they have something to say; fools because they have to say something.",
        "Gaga Gougou Gougou Dada",
        "Quatre journaux hostiles sont plus a craindre que mille baionnettes."
    ]
    ciphertexts = []

    def test_reversible_direct(self):
        for plaintext in self.plaintexts:
            self.assertEqual(plaintext, self.cipher.decipher(self.cipher.encipher(plaintext)))

    def test_reversible_inverse(self):
        for ciphertext in self.ciphertexts:
            self.assertEqual(ciphertext, self.cipher.encipher(self.cipher.decipher(ciphertext)))

    def test_enciphering(self):
        for sentence, cypher in zip(self.plaintexts, self.ciphertexts):
            self.assertEqual(cypher, self.cipher.encipher(sentence))

    def test_deciphering(self):
        for sentence, cypher in zip(self.plaintexts, self.ciphertexts):
            self.assertEqual(sentence, self.cipher.decipher(cypher))


class TestShapeCipher(TestStreamCipher):

    plaintexts = [
        "ABCDEFGHIKLMNOPQRSTUVWXYZ",
        #"ABCDE\nFGHIK\nLMNOP\nQRSTU\nVWXYZ"
    ]


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
