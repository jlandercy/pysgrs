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


dummy_space = ParameterSpace(
    text=[
        "LA VIE EST UNE ETRANGE ENTREPRISE, PLEINE DE RISQUES ET SANS BUT REVELE.",
        "LA CRYPTOGRAPHIE EST UNE SUPERBE DISCIPLINE ET EGALEMENT LE REFLET DE NOS LIMITES.",
        "JE N'AI D'YEUX QUE POUR TOI, L'AMOUR REND AVEUGLE N'EST-CE PAS ?",
        "LA TELEVISION REND BETE ET MECHANT SURTOUT LES EMISSIONS FAITES PAR DES CONS POUR LES CONS.",
        "JULES N'A PAS RECU DE CEASAR CETTE ANNEE, PERSONNE NE SAIT SI ON LE REVERA A CANNES."
    ],
    seed=[123456789],
    key=["A", "AB", "ABC", "ABCD", "ABCDE"],
    population_size=[50, 100, 150, 200],
    threshold=[0.5],
    weights=[[0.6, 0.3, 0.1]]
)

if __name__ == "__main__":

    for p in dummy_space.generate():
        print(p)
    print(dummy_space.size())
