import sys
import unittest

from pysgrs import errors
from pysgrs import settings


class TestStreamCypher:

    cypher = None
    sentences = [
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

    def test_reversible_direct(self):
        for sentence in self.sentences:
            self.assertEqual(sentence, self.cypher.decypher(self.cypher.cypher(sentence)))

    def test_reversible_inverse(self):
        for cypher in self.cyphers:
            self.assertEqual(cypher, self.cypher.cypher(self.cypher.decypher(cypher)))

    def test_cyphering(self):
        for sentence, cypher in zip(self.sentences, self.cyphers):
            self.assertEqual(cypher, self.cypher.cypher(sentence))

    def test_decyphering(self):
        for sentence, cypher in zip(self.sentences, self.cyphers):
            self.assertEqual(sentence, self.cypher.decypher(cypher))


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
