import sys
import unittest


class TestCypher:

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
        "Wise men speak because they have something to say; fools because they have to say something."
    ]

    def setUp(self):
        pass

    def test_reversible_cypher(self):
        for sentence in self.sentences:
            self.assertEqual(self.cypher.decypher(self.cypher.cypher(sentence)), sentence)

    def test_cyphering(self):
        for sentence, cypher in zip(self.sentences, self.cyphers):
            self.assertEqual(self.cypher.cypher(sentence), cypher)


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
