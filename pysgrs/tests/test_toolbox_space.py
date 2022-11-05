import unittest

import numpy as np

from pysgrs import alphabets
from pysgrs import toolbox
from pysgrs import texts


class TestParameterSpaceGeneration(unittest.TestCase):

    def setUp(self) -> None:
        self.parameters = dict(
            text=texts.small_sentences_fr,
            key=["A", "AB", "ABC", "ABCD", "ABCDE"],
            seed=[123456789],
            population_size=[50, 100, 150, 200],
            threshold=[0.5],
            weights=[[0.6, 0.3, 0.1]]
        )
        self.space = toolbox.ParameterSpace(**self.parameters)

    def test_generate_parameters_as_dict(self):
        for parameter in self.space.generate():
            self.assertIsInstance(parameter, dict)
            self.assertSetEqual(set(parameter.keys()), set(self.parameters.keys()))

    def test_generate_parameters_as_tuple(self):
        for parameter in self.space.generate(mode="tuple"):
            self.assertIsInstance(parameter, tuple)
            self.assertEqual(len(parameter), len(self.parameters))

    def test_space_size(self):
        self.assertEqual(self.space.size(), np.prod([len(value) for value in self.parameters.values()]))


class TestKeySpaceGeneration(unittest.TestCase):

    def setUp(self) -> None:
        self.space = toolbox.KeySpace(
            alphabet=alphabets.BasicAlphabet(),
            min_key_size=1,
            max_key_size=3,
        )
        np.random.seed(123)

    def test_space_generation(self):
        for key in self.space.generate():
            self.assertIsInstance(key, dict)
            self.assertSetEqual(set(key.keys()), {"key_size", "key"})

    def test_key_sizes(self):
        self.assertTrue(np.allclose(self.space.key_sizes, [1, 2, 3]))

    def test_key_space_sizes(self):
        self.assertTrue(np.allclose(self.space.key_space_sizes, [26**1, 26**2, 26**3]))

    def test_space_size(self):
        size = 26**1 + 26**2 + 26**3
        self.assertEqual(self.space.size(), size)
        self.assertEqual(len(list(self.space.generate(mode="tuple"))), size)

    def test_sample_key_size(self):
        sizes = self.space.sample_key_size(size=300000)
        exact = np.sum(self.space.key_space_sizes*self.space.key_sizes)/self.space.size()
        self.assertTrue(np.isclose(np.mean(sizes), exact, rtol=0.001))

    def test_sample_key(self):
        keys = self.space.sample(size=20)
        self.assertTrue(all([self.space.min_key_size <= len(key) <= self.space.max_key_size for key in keys]))
