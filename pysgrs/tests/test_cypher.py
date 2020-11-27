import sys
import unittest


class TestCypher:

    cypher = None
    sentences = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
        "WALTZBADNYMPHFORQUICKJIGSVEX",
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
