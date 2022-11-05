import abc


class SelectionOperator(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def select(population, scores, size=1, **kwargs):
        pass


class CrossoverOperator(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def crossover(*parents, **kwargs):
        pass


class MutationOperator:

    @staticmethod
    @abc.abstractmethod
    def mutate(individual, **kwargs):
        pass
