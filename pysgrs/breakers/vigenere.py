import time
import uuid
import hashlib

import numpy as np
import pandas as pd
from scipy.spatial import distance

from pysgrs import scores
from pysgrs.toolbox import AsciiCleaner, FrequencyAnalyzer
from pysgrs.alphabets import BasicAlphabet
from pysgrs.toolbox.spaces import KeySpace
from pysgrs.toolbox import operators
from pysgrs.interfaces import GenericBreaker
from pysgrs.ciphers import VigenereCipher


class VigenereGeneticAlgorithmBreaker:

    cipher_factory = VigenereCipher
    key_space_factory = KeySpace

    def __init__(
        self,
        selection_operator=operators.RouletteWheelSelection,
        crossover_operator=operators.SinglePointCrossover,
        mutation_operator=operators.TworsMutation,
        score_function=scores.mixed_ngrams_fr,
        alphabet=BasicAlphabet(),
        language="fr"
    ):

        # Setup:
        self.alphabet = alphabet
        self.language = language

        # Genetic Algorithm requirements:
        self.selection_operator = selection_operator
        self.crossover_operator = crossover_operator
        self.mutation_operator = mutation_operator
        self.score_function = score_function

        # Memoization:
        self.memory = dict()

    @staticmethod
    def guess_key_sizes(text, min_key_size=1, max_key_size=48, normalize=False, order_by="max", ascending=False):
        if normalize:
            text = AsciiCleaner.normalize(text)
        coincidences = FrequencyAnalyzer.keysize_coincidences(
            text, min_key_size=min_key_size, max_key_size=max_key_size
        )
        guesses = coincidences.groupby("key_size")["coincidence"].agg(
            ["min", "mean", "median", "max"]
        )
        #guesses["score"] = guesses["mean"] + guesses["median"] + (guesses["min"] + guesses["max"])/guesses["max"]
        guesses = guesses.sort_values(order_by, ascending=ascending)
        #guesses.columns = guesses.columns.map(lambda x: "coincidence_" + x)
        return guesses

    @staticmethod
    def guess_key_size(text, min_key_size=1, max_key_size=48, normalize=False, order_by="max"):
        return VigenereGeneticAlgorithmBreaker.guess_key_sizes(
            text, min_key_size=min_key_size, max_key_size=max_key_size, normalize=normalize, order_by=order_by
        ).index[0]

    def score_text(self, cipher_text, key, memoization=False):

        # Memory restitution:
        if memoization:
            if key in self.memory:
                return self.memory[key]

        # Compute:
        factory = self.cipher_factory(key=key)
        text = factory.decipher(cipher_text)
        score = self.score_function.score(text)
        result = {
            "key": key,
            "score": score,
            "text": text,
        }

        # Memory storage:
        if memoization:
            self.memory[key] = result

        return result

    def score_texts(self, cipher_text, keys, memoization=False):
        results = pd.DataFrame([self.score_text(cipher_text, key, memoization=memoization) for key in keys])
        results = results.sort_values("score", ascending=False).reset_index(drop=True)
        return results

    def attack(
        self,
        cipher_text, key_size=None, memoization=True,
        seed=None, population_size=200, max_steps=300,
        elitism_ratio=None, elitism_size=2, crossover_probability=0.5, mutation_probability=0.1,
        halt_on_score_threshold=None, halt_on_exact_key=None, halt_on_convergence=True,
    ):

        def step_logger():
            return {
                "timestamp": pd.Timestamp.now().isoformat(),
                "cipher_text_hash": cipher_text_hash,
                "attack_id": attack_id,
                "language": self.language,
                "seed": seed,
                "memoization": memoization,
                "step_index": step_index,
                "max_steps": max_steps,
                "step_time_ms": (toc - tic) / 1e6,
                "population_size": population.shape[0],
                "elitism_size": elitism_size,
                "key_space_size": key_space_size,
                "memory_size": len(self.memory),
                "alphabet": self.alphabet.__class__.__name__,
                "score_function": self.score_function.__class__.__name__,
                "selection_operator": self.selection_operator.__name__,
                "crossover_operator": self.crossover_operator.__name__,
                "mutation_operator": self.mutation_operator.__name__,
                "crossover_probability": crossover_probability,
                "mutation_probability": mutation_probability,
                "alphabet_size": alphabet_size,
                "cipher_text_size": cipher_text_size,
                "key_size": key_size,
                "min_score": population.iloc[-1, :]["score"],
                "max_score": population.iloc[0, :]["score"],
                "best_key": population.iloc[0, :]["key"],
                #"best_text": population.iloc[0, :]["text"],
                "best_text_short": population.iloc[0, :]["text"][:256].replace("\n", " ").replace("\t", " ")
            }

        # Attack identifier and Cipher Text hash:
        attack_id = uuid.uuid4().hex
        cipher_text_hash = hashlib.sha256(cipher_text.encode()).hexdigest()

        # Guess key size if not known:
        if key_size is None:
            key_size = self.guess_key_size()

        # Set the seed before the attack for reproducibility sake:
        if seed is not None:
            np.random.seed(seed)

        # Create the key space:
        key_space = self.key_space_factory(alphabet=self.alphabet, min_key_size=key_size)
        key_space_size = key_space.size()

        # Relevant Sizes:
        alphabet_size = self.alphabet.size
        cipher_text_size = len(cipher_text)

        # Elitism size:
        if elitism_size is None:
            if elitism_ratio is None:
                elitism_size = 0
            else:
                elitism_size = int(elitism_ratio*population_size)

        # Initial population:
        step_index = 0
        tic = time.time_ns()
        population = self.score_texts(cipher_text, keys=key_space.sample(size=population_size), memoization=memoization)
        toc = time.time_ns()
        yield step_logger()

        # Generate new populations:
        for step_index in np.arange(1, max_steps + 1):

            # Start new generation:
            tic = time.time_ns()

            # Selection for reproduction:
            selection = self.selection_operator.select(
                population["key"].values,
                population["score"].values,
                size=population_size
            )

            # Crossover & Mutation:
            offspring = []
            batch_size = len(selection) // 2
            for pair in zip(selection[batch_size:], selection[:batch_size]):
                offspring.extend([
                    self.mutation_operator.mutate(individual, probability=mutation_probability)
                    for individual in self.crossover_operator.crossover(
                        *pair,
                        probability=crossover_probability,
                        symbols=self.alphabet.symbols
                    )
                ])
            offspring = self.score_texts(cipher_text, keys=offspring, memoization=memoization)

            # Elitism:
            population = pd.concat([
                population.iloc[:elitism_size, :],
                offspring
            ]).sort_values("score", ascending=False)
            population = population.iloc[:population_size, :]

            # End of new generation:
            toc = time.time_ns()

            # Extra Stop Criteria:

            # Dispatch step information:
            step = step_logger()
            yield step

            # Break on convergence (potentially trapped in local minimum):
            if halt_on_convergence and (step["min_score"] == step["max_score"]):
                break

            # Break on score threshold:
            if (halt_on_score_threshold is not None) and (step["max_score"] >= halt_on_score_threshold):
                break

            # Break if known key is found:
            if (halt_on_exact_key is not None) and (step["best_key"] == halt_on_exact_key):
                break
