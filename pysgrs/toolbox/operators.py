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
        fitness = np.power(1/np.array(scores), 2)
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
        point = np.random.randint(0, key_size)

        # Single point swap:
        child_1 = parent_1[:point] + parent_2[point:]
        child_2 = parent_2[:point] + parent_1[point:]

        return child_1, child_2


class UniformCrossover(CrossoverOperator):
    @staticmethod
    def crossover(parent_1, parent_2, probability=0.5, **kwargs):
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


class RandomMutation(MutationOperator):
    @staticmethod
    def mutate(individual, probability=0.01, symbols=None, **kwargs):
        """
        Randomly change genes using symbols with a defined probability rate
        """

        if symbols is None:
            symbols = individual
        symbols = list(symbols)

        key_size = len(individual)

        mutated = list(individual)
        for i in range(key_size):
            if np.random.uniform() >= (1. - probability):
                mutated[i] = np.random.choice(symbols)

        if isinstance(individual, str):
            mutated = "".join(mutated)

        return mutated


class TworsMutation(MutationOperator):
    @staticmethod
    def mutate(individual, probability=0.05, **kwargs):
        """Swap to genes within the genome"""

        if np.random.uniform() >= (1. - probability):

            # Mutation Points:
            key_size = len(individual)
            point_1 = np.random.randint(0, key_size - 1)
            point_2 = np.random.randint(0, key_size - 1)

            child = list(individual)
            child[point_2], child[point_1] = child[point_1], child[point_2]

            if isinstance(individual, str):
                child = "".join(child)

            return child

        return individual
