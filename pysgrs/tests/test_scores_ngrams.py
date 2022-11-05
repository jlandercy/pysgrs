import unittest

import numpy as np

from pysgrs import texts
from pysgrs import scores


class GenericScoreTest:

    _texts = texts.small_sentences_fr
    _score = None

    def test_scalar_score(self):
        for text in self._texts:
            score = self._score.score(text)
            self.assertIsInstance(score, float)

    def test_negative_score(self):
        for text in self._texts:
            score = self._score.score(text)
            self.assertTrue(score < 0.)


class TestScore1Gram(GenericScoreTest, unittest.TestCase):
    _score = scores.NGramScore(order=1, language="fr")


class TestScore2Gram(GenericScoreTest, unittest.TestCase):
    _score = scores.NGramScore(order=2, language="fr")


class TestScore3Gram(GenericScoreTest, unittest.TestCase):
    _score = scores.NGramScore(order=3, language="fr")


class TestScoreMixedNGram(GenericScoreTest, unittest.TestCase):
    _score = scores.MixedNGramScore(weights=[0.6, 0.3, 0.1], language="fr")
