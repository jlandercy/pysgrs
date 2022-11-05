import itertools


class ParameterSpace:

    def __init__(self, **parameters):
        self._paramaters = parameters

    @property
    def parameters(self):
        return self._paramaters

    def generate(self, mode="dict"):
        for parameter in itertools.product(*[value for value in self.parameters.values()]):
            if mode == "dict":
                yield {key: value for key, value in zip(self.parameters.keys(), parameter)}
            else:
                yield parameter

    def size(self):
        count = 0
        for _ in self.generate():
            count += 1
        return count


if __name__ == "__main__":

    space = ParameterSpace(a=[1, 2, 3], b=["a", "b"])
    for p in space.generate():
        print(p)

    print(space.size())
