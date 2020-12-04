import sys
import unittest

from pysgrs import toolbox
from pysgrs import errors
from pysgrs import settings


class TestFormatShaper(unittest.TestCase):

    sentences = [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY\nZ",
        "ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY\nZ    ",
    ]

    def setUp(self):
        self.shaper = toolbox.Shaper

    def test_to_matrix(self):
        for sentence in self.sentences:
            print(sentence)
            r = self.shaper.to_matrix(sentence)
            print(r)


class TestFormatShaperSpecialCase(unittest.TestCase):

    def setUp(self):
        self.shaper = toolbox.Shaper

    def test_shape_string_auto_square(self):
        x = self.shaper.to_matrix("ABCDEFGIH")
        self.assertEqual((3, 3), x.shape)


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
