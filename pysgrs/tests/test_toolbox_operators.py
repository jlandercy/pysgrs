import unittest

import numpy as np

from pysgrs import alphabets
from pysgrs import toolbox
from pysgrs import spaces
from pysgrs import scores
from pysgrs import texts


class GenericSelectionOperatorTest:

    _seed = 123
    _size = 10
    _operator = None
    _generator = None
    _score = None
    _parameters = {}

    def setUp(self) -> None:
        # Fix seed:
        np.random.seed(self._seed)
        # Generate population and assess score:
        self.population = self._generator.sample(size=2*self._size)
        self.scores = [self._score.score(individual) for individual in self.population]

    def test_selection_operator(self):
        selection = self._operator.select(self.population, self.scores, size=self._size, **self._parameters)
        self.assertIsInstance(selection, list)
        self.assertEqual(len(selection), self._size)


class TestNumerusClaususSelectionOperator(GenericSelectionOperatorTest, unittest.TestCase):
    _operator = toolbox.NumerusClaususSelection
    _generator = spaces.basic_space_10
    _score = scores.mixed_ngrams_fr


class TestRouletteWheelSelectionOperator(GenericSelectionOperatorTest, unittest.TestCase):
    _operator = toolbox.RouletteWheelSelection
    _generator = spaces.basic_space_10
    _score = scores.mixed_ngrams_fr


class GenericCrossoverOperatorTest:

    _seed = 123
    _size = 200
    _operator = None
    _generator = None
    _parameters = {}

    def setUp(self) -> None:
        # Fix seed:
        np.random.seed(self._seed)
        # Generate population and assess score:
        self.parent_tuples = [
            pair for pair in zip(self._generator.sample(size=self._size), self._generator.sample(size=self._size))
        ]

    def test_crossover_operator(self):
        for parents in self.parent_tuples:
            children = self._operator.crossover(*parents, *self._parameters)
            #print(*parents, " -> ", *children)
            self.assertTrue(all([len(child) == len(children[0]) for child in children]))


class TestSinglePointCrossoverOperator(GenericCrossoverOperatorTest, unittest.TestCase):
    _operator = toolbox.SinglePointCrossover
    _generator = spaces.basic_space_10


class TestUniformCrossoverOperator(GenericCrossoverOperatorTest, unittest.TestCase):
    _operator = toolbox.UniformCrossover
    _generator = spaces.basic_space_10


class GenericMutationOperatorTest:

    _seed = 123
    _size = 200
    _operator = None
    _generator = None
    _parameters = {}

    def setUp(self) -> None:
        # Fix seed:
        np.random.seed(self._seed)
        # Generate population and assess score:
        self.population = self._generator.sample(size=self._size)

    def test_mutation_operator(self):
        for individual in self.population:
            mutated = self._operator.mutate(individual, *self._parameters)
            #print(individual, " -> ", mutated)
            self.assertEqual(len(individual), len(mutated))


class TestTworsMutationOperator(GenericMutationOperatorTest, unittest.TestCase):
    _operator = toolbox.TworsMutation
    _generator = spaces.basic_space_10

