from operator import itemgetter

import numpy as np

from pysgrs.interfaces.operator import SelectionOperator, CrossoverOperator, MutationOperator


class NumerusClaususSelection(SelectionOperator):
    @staticmethod
    def select(population, scores, size=1, **kwargs):
        """
        Sort population by scores, keep only best individuals up to size
        """
        order = np.argsort(scores)
        sorted_population = list(itemgetter(*order)(population))
        return sorted_population[-size:]


class RouletteWheelSelection(SelectionOperator):
    @staticmethod
    def select(population, scores, size=1, scale=1., bias=0.1, **kwargs):
        """
        Perform roulette wheel selection (random choice with replacement weighted by likelihood)
        """
        min_score = np.min(scores)
        extent = np.max(scores) - min_score
        fitness = scale*(np.array(scores) - min_score)/extent + bias
        probabilities = fitness/np.sum(fitness)
        selection = np.random.choice(population, p=probabilities, size=size)
        return list(selection)


class SinglePointCrossover(CrossoverOperator):
    @staticmethod
    def crossover(parent_1, parent_2, **kwargs):
        """
        Swap part of genomes among parents on a single cross point
        """

        if len(parent_1) != len(parent_2):
            ValueError("Parents must have the same size")

        # Cross Point:
        key_size = len(parent_1)
        point = np.random.random_integers(0, key_size)

        # Single point swap:
        child_1 = parent_1[:point] + parent_2[point:]
        child_2 = parent_2[:point] + parent_1[point:]

        return child_1, child_2


class UniformCrossover(CrossoverOperator):
    @staticmethod
    def crossover(parent_1, parent_2, probability=0.1, **kwargs):
        """
        Swap corresponding genes among parents with defined probability
        """

        if len(parent_1) != len(parent_2):
            ValueError("Parents must have the same size")

        key_size = len(parent_1)

        child_1, child_2 = list(parent_1), list(parent_2)
        for i in range(key_size):
            if np.random.uniform() >= (1. - probability):
                child_2[i], child_1[i] = child_1[i], child_2[i]

        if isinstance(parent_1, str):
            child_1, child_2 = "".join(child_1), "".join(child_2)

        return child_1, child_2


class UniformMutation(MutationOperator):
    @staticmethod
    def mutate(individual, **kwargs):
        pass


class RandomMutation(MutationOperator):
    @staticmethod
    def mutate(individual, **kwargs):
        """
        Randomly change genes
        """
        pass


class TworsMutation(MutationOperator):
    @staticmethod
    def mutate(individual, **kwargs):
        """Swap to genes within the genome"""
        pass
