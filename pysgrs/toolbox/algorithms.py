import sys

from pysgrs.settings import settings


class Algorithm:
    pass


class HillClimbingAlgorithm(Algorithm):
    pass


class GeneticAlgorithm(Algorithm):
    """
    https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3
    START
    Generate the initial population
    Compute fitness
    REPEAT
        Selection
        Crossover
        Mutation
        Compute fitness
    UNTIL population has converged
    STOP
    """

    def __init__(self):
        pass

    def select(self):
        pass

    def crossover(self):
        pass

    def mutate(self):
        pass

    def fitness(self):
        pass


def main():
    settings.logger.warning("Hello world!")
    sys.exit(0)


if __name__ == "__main__":
    main()
