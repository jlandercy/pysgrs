import sys
import unittest

import numpy as np

from pysgrs import toolbox
from pysgrs import errors
from pysgrs import settings


class TestModularArithmetic(unittest.TestCase):

    gcd_values = [
        ((54, 24), 6),
        ((12, 8), 4),
        ((13, 17), 1),
        ((60, 36), 12),
        ((60, 32), 4),
        ((60, 30), 30),
    ]

    modinv_values = [
        ((3504, 385), 79),
        ((8, 5), 2),
        ((29, 7), 1),
        ((67, 13), 7),
    ]

    def test_gcd(self):
        for value in self.gcd_values:
            self.assertEqual(value[1], toolbox.ModularArithmetic.gcd(*value[0]))

    def test_egcd(self):
        for value in self.gcd_values:
            self.assertEqual(value[1], toolbox.ModularArithmetic.egcd(*value[0])[0])

    def test_modinv(self):
        for value in self.modinv_values:
            self.assertEqual(value[1], toolbox.ModularArithmetic.modinv(*value[0]))


class TestFormatShaper(unittest.TestCase):

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


class TestHelperCleanerStripAccents(unittest.TestCase):

    sentences = [
        ("áàâäã", "aaaaa"),
        ("éèêë", "eeee"),
        ("íìîï", "iiii"),
        ("óòôöõ", "ooooo"),
        ("úùûü", "uuuu"),
        ("ç", "c")
    ]

    def test_sentence_cleaning(self):
        for sentence in self.sentences:
            self.assertEqual(sentence[1], toolbox.Cleaner.strip_accents(sentence[0]))
            self.assertEqual(sentence[1].upper(), toolbox.Cleaner.strip_accents(sentence[0].upper()))


class TestHelperCleanerRemovePunctuation(unittest.TestCase):

    sentences = [
        ("Cette phrase - bien qu'ennuyeuse - sert de test: vous pouvez vérifiez!",
         "Cette phrase bien qu ennuyeuse sert de test vous pouvez vérifiez"),
        ("Les  espaces ne sont: pas:forcément bien mis  , allez savoir après,plusieurs!manipulations...",
         "Les espaces ne sont pas forcément bien mis allez savoir après plusieurs manipulations")
    ]

    def test_sentence_cleaning(self):
        for sentence in self.sentences:
            self.assertEqual(sentence[1], toolbox.Cleaner.remove_punctuation(sentence[0]))


def main():
    unittest.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
