import unittest

import numpy as np
import pandas as pd

from pysgrs import breakers
from pysgrs import scores
from pysgrs import texts
from pysgrs import toolbox


pd.options.display.max_columns = 60
pd.options.display.max_rows = 300


class GenericVigenereBreakerTest:

    breaker_factory = breakers.VigenereGeneticAlgorithmBreaker
    parameters_space = toolbox.ParameterSpace(
        seed=[1234567, 8901234, 5678901],
        text=texts.small_sentences_fr,
        key=["SECRET", "SECRETTOKEN", "THECOLLATZCONJECTURE"],
        mutation_operator=[toolbox.TworsMutation, toolbox.RandomMutation],
        mutation_probability=[0.01, 0.1, 0.25],
        score_function=[scores.mixed_ngrams_fr]
    )

    def generate(self):
        for parameters in self.parameters_space.generate():
            parameters["cipher"] = self.breaker_factory.cipher_factory(key=parameters["key"])
            parameters["cipher_text"] = parameters["cipher"].encipher(toolbox.AsciiCleaner.strip_accents(parameters["text"]))
            self.assertEqual(parameters["text"], parameters["cipher"].decipher(parameters["cipher_text"]))
            yield parameters


class BasicVigenereGeneticAlgorithmBreaker(GenericVigenereBreakerTest, unittest.TestCase):

    def test_cipher_attack(self):

        for parameters in self.generate():

            results = []
            for step in self.breaker_factory(
                score_function=parameters["score_function"],
                mutation_operator=parameters["mutation_operator"]
            ).attack(
                parameters["cipher_text"],
                seed=parameters["seed"],
                key_size=len(parameters["key"]),
                mutation_probability=parameters["mutation_probability"],
                halt_on_exact_key=parameters["key"],
            ):
                results.append(step)
                print("{step_index}/{max_steps}\t{step_time_ms: 10.3f} ms\t{memory_size}\t{population_size}\t{key_size}\t{mutation_probability}\t{min_score}\t{max_score}\t{best_key}\t{best_text_short}".format(**step))

            results = pd.DataFrame(results)
            results.to_excel("./media/attack_%s.xlsx" % step["attack_id"])

            #break
