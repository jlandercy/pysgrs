import sys
import unittest

import numpy as np

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
            r = self.shaper.to_matrix(sentence)


class TestFormatShaperInputsOutputs(unittest.TestCase):

    def setUp(self):
        self.shaper = toolbox.Shaper

    def test_shape_string_auto_square(self):
        for i in range(10):
            x = self.shaper.to_matrix("A"*((i+1)**2))
            self.assertEqual((i+1, i+1), x.shape)

    def test_shape_string_auto_rectangle(self):
        for i in range(10):
            x = self.shaper.to_matrix("A"*((i+1)*(i+2)))
            self.assertEqual((i+1, i+2), x.shape)

    def test_shape_string_user_shape(self):
        for i in range(10):
            x = self.shaper.to_matrix("A"*((i+1)*(i+2)+1), shape=(i+2, i+2))
            self.assertEqual((i+2, i+2), x.shape)

    def test_shape_block_auto(self):
        for i in range(10):
            s = "\n".join(["A"*(i+1)]*5 + ["B"])
            x = self.shaper.to_matrix(s)
            self.assertEqual((6, i+1), x.shape)

    def test_shape_block_user_shape(self):
        for i in range(10):
            s = "\n".join(["A"*(i+1)]*5 + ["B"])
            x = self.shaper.to_matrix(s, shape=(i+1, 6))
            self.assertEqual((i+1, 6), x.shape)

    def test_shape_matrix_auto(self):
        for i in range(10):
            x = np.array([list("A"*(i+1))]*5 + [list("B"*(i+1))])
            x = self.shaper.to_matrix(x)
            self.assertEqual((6, i+1), x.shape)

    def test_shape_matrix_user_shape(self):
        for i in range(10):
            x = np.array([list("A"*(i+1))]*5 + [list("B"*(i+1))])
            x = self.shaper.to_matrix(x, shape=(i+1, 6))
            self.assertEqual((i+1, 6), x.shape)


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
