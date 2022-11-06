import unittest
import pprint

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
        seed=[123456789, 987654321, 546987123],
        text=texts.small_text_fr,
        key=["SECRET", "SECRETTOKEN", "GENETICALGORITHM", "THECOLLATZCONJECTURE", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
        max_steps=[50],
        population_size=[50, 100, 250, 500],
        elitism_ratio=[0.1, 1.0],
        elitism_size=[None],
        mutation_operator=[toolbox.TworsMutation, toolbox.RandomMutation],
        mutation_probability=[0.01, 0.1, 0.25],
        score_function=[
            scores.mixed_ngrams_fr,
            #scores.mixed_ngrams_1_fr,
            #scores.mixed_ngrams_2_fr,
            #scores.mixed_ngrams_3_fr
        ]
    )

    def generate(self):
        for parameters in self.parameters_space.generate():
            parameters["cipher"] = self.breaker_factory.cipher_factory(key=parameters["key"])
            parameters["text"] = toolbox.AsciiCleaner.strip_accents(parameters["text"])
            parameters["cipher_text"] = parameters["cipher"].encipher(parameters["text"])
            self.assertEqual(parameters["text"], parameters["cipher"].decipher(parameters["cipher_text"]))
            yield parameters


class BasicVigenereGeneticAlgorithmBreaker(GenericVigenereBreakerTest, unittest.TestCase):

    def test_cipher_attack(self):

        run_size = self.parameters_space.size()

        tests = []
        for run_index, parameters in enumerate(self.generate()):

            pprint.pprint(parameters)

            results = []
            for step in self.breaker_factory(
                ** {key: parameters[key] for key in [
                    "selection_operator", "crossover_operator", "mutation_operator", "score_function",
                    "alphabet", "language"
                ] if key in parameters}
            ).attack(
                parameters["cipher_text"],
                key_size=len(parameters["key"]),
                halt_on_exact_key=parameters["key"],
                **{key: parameters[key] for key in [
                    "seed", "population_size", "max_steps", "elitism_ratio", "elitism_size",
                    "crossover_probability", "mutation_probability"
                ] if key in parameters}
            ):
                results.append(step)
                print("{run_index}/{run_size}\t{step_index}/{max_steps}\t{step_time_ms: 10.3f} ms\t{memory_size}\t{population_size}\t{key_size}\t{mutation_probability}\t{min_score}\t{max_score}\t{best_key}\t{best_text_short}".format(**step, run_size=run_size, run_index=run_index))

            results = pd.DataFrame(results).assign(run_index=run_index, run_size=run_size)
            results.to_excel("./media/steps/attack_%s.xlsx" % step["attack_id"])
            tests.append(results)

            #break
        tests = pd.concat(tests)
        tests.to_excel("./media/attack.xlsx")
