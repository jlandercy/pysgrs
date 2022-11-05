import time
import uuid

import numpy as np
import pandas as pd
from scipy.spatial import distance

from pysgrs import scores
from pysgrs.toolbox import AsciiCleaner, FrequencyAnalyzer
from pysgrs.alphabets import BasicAlphabet
from pysgrs.toolbox.spaces import KeySpace
from pysgrs.toolbox.operators import RouletteWheelSelection, SinglePointCrossover, TworsMutation
from pysgrs.interfaces import GenericBreaker
from pysgrs.ciphers import VigenereCipher


class VigenereGeneticAlgorithmBreaker_v1:

    def __init__(self, score, alphabet=BasicAlphabet(), language="fr"):
        self.score = score
        self.factory = VigenereCipher
        self.alphabet = alphabet
        self.language = language

    def guess_key_sizes(self, text, min_key_size=1, max_key_size=48, normalize=True, order_by="min"):
        if normalize:
            text = AsciiCleaner.normalize(text)
        coincidences = FrequencyAnalyzer.keysize_coincidences(
            text, min_key_size=min_key_size, max_key_size=max_key_size
        )
        guesses = coincidences.groupby("key_size")["coincidence"].agg(
            ["min", "mean", "median", "max"]
        ).sort_values(order_by, ascending=False)
        guesses.columns = guesses.columns.map(lambda x: "coincidence_" + x)
        return guesses

    def random_population(self, key_size, population_size=20):
        return ["".join(np.random.choice(list(self.alphabet.symbols), size=key_size)) for i in range(population_size)]

    def make_pairs(self, group):
        group = np.array(group)
        np.random.shuffle(group)
        n = group.size//2
        return [pair for pair in zip(group[:n], group[n:])]

    def random_index(self, key_size):
        return np.random.choice(range(key_size))

    def swap_gene(self, old_1, old_2, index):
        new_1, new_2 = list(old_1), list(old_2)
        new_1[index], new_2[index] = new_2[index], new_1[index]
        return "".join(new_1), "".join(new_2)

    def double_cross_mutation(self, old_1, old_2):
        """
        S. S.Omran, A Cryptanalytic Attack on Vigenère Cipher Using Genetic Algorithm
        """
        i, j = self.random_index(len(old_1)), self.random_index(len(old_2))
        i, j = min(i, j), max(i, j)
        new_1 = list(old_1)
        new_2 = list(old_2)
        new_1[i] = old_2[j]
        new_1[j] = old_2[i]
        new_2[i] = old_1[j]
        new_2[j] = old_1[i]
        return "".join(new_1), "".join(new_2)

    def single_point_crossover(self, old_1, old_2, threshold=0.8, mutation=double_cross_mutation):
        """
        Single-Point Crossover w/ Mutation
        """
        index = self.random_index(len(old_1))
        new_1 = old_1[:index] + old_2[index:]
        new_2 = old_2[:index] + old_1[index:]
        if np.random.rand() >= threshold:
            new_1, new_2 = mutation(self, new_1, new_2)
        return new_1, new_2

    def uniform_crossover(self, old_1, old_2, threshold=0.5):
        """
        Uniform cross-over
        """
        pass

    def group_crossover(self, group, threshold=0.8, crossover=single_point_crossover):
        new_group = []
        for pair in self.make_pairs(group):
            new_pair = crossover(self, *pair, threshold=threshold)
            new_group.extend(new_pair)
        return new_group

    def score_group(self, text, group):
        return [self.score.score(VigenereCipher(key=key).decipher(text)) for key in group]

    def attack_with_key_size_guess(self, text, min_key_size=10, max_key_size=48, order_by="min", max_guess=5, **kwargs):
        key_sizes = self.guess_key_sizes(
            text, min_key_size=min_key_size, max_key_size=max_key_size, order_by=order_by
        ).reset_index()
        for key_size in key_sizes.iloc[:max_guess].to_dict(orient='records'):
            for record in self.attack(text, key_size=key_size["key_size"], **kwargs):
                record.update(key_size)
                yield record

    def attack(self, text, key_size=None, population_size=20, generation_count=30, threshold=0.8,
               score_threshold=None, exact_key=None, seed=None, stop_on_convergence=False,
               crossover=single_point_crossover):

        # Attack identifier
        identifier = uuid.uuid4().hex

        # Set seed to make attack reproducible
        if seed is not None:
            np.random.seed(seed)

        # Create random population:
        initial_group = self.random_population(key_size, population_size=population_size)
        initial_scores = self.score_group(text, initial_group)

        for i in range(generation_count):

            tic = time.time_ns()

            # Create a new population by crossing and mutating:
            new_group = self.group_crossover(initial_group, threshold=threshold, crossover=crossover)
            new_scores = self.score_group(text, new_group)

            # Merge groups:
            group = initial_group + new_group
            group_scores = initial_scores + new_scores
            index = np.argsort(group_scores)

            # Keep best representative:
            initial_group = list(np.array(group)[index][population_size:])
            initial_scores = list(np.array(group_scores)[index][population_size:])

            toc = time.time_ns()

            generation = {
                "seed": seed,
                "identifier": identifier,
                "generation": i+1,
                "generation_count": generation_count,
                "threshold": threshold,
                "key_size": key_size,
                "population_size": population_size,
                "global_min": np.min(group_scores),
                "global_max": np.max(group_scores),
                "selection_min": np.min(initial_scores),
                "selection_max": np.max(initial_scores),
                "best_key": initial_group[-1],
                "elapsed": (toc - tic)/1e9
                #"group": group,
            }
            print("{generation}/{generation_count:}\t{elapsed:.3f}\t{seed:}\t{population_size:}\t{key_size:}\t{threshold:}\t{selection_min:.3f}\t{selection_max:.3f}\t{best_key:}".format(**generation))
            yield generation

            # Extra stop criteria:

            # Trapped in local min:
            if stop_on_convergence and (generation["selection_min"] == generation["selection_max"]):
                break

            # No crossing possible all the same:
            if all([initial_group[-1] == key for key in initial_group]):
                break

            # Score threshold:
            if (score_threshold is not None) and (generation["selection_max"] >= score_threshold):
                break

            # Key found:
            if (exact_key is not None) and (generation["best_key"] == exact_key):
                break


class VigenereGeneticAlgorithmBreaker:

    cipher_factory = VigenereCipher
    key_space_factory = KeySpace

    def __init__(
        self,
        selection_operator=RouletteWheelSelection,
        crossover_operator=SinglePointCrossover,
        mutation_operator=TworsMutation,
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

    def guess_key_size(self, text):
        return 10

    def attack(
        self,
        cipher_text, key_size=None,
        seed=None, population_size=50, max_steps=50, crossover_probability=0.1, mutation_probability=0.1,
        halt_score_threshold=None, halt_exact_key=None, halt_on_convergence=True,
    ):

        # Attack identifier:
        attack_id = uuid.uuid4().hex

        # Guess key size if not known:
        if key_size is None:
            key_size = self.guess_key_size()

        # Fix the seed before the attack for reproducibility sake:
        if seed is not None:
            np.random.seed(seed)

        # Create the key space:
        key_space = self.key_space_factory(alphabet=self.alphabet, min_key_size=key_size)
        print("Key Space Size: %d" % key_space.size())

        # Start the attack:
        population = key_space.sample(size=population_size)
        print(population)

        # Generate new populations:
        for step_index in range(max_steps + 1):

            # Decipher text for each individual and assess fitness:
            tic = time.time_ns()
            texts = [self.cipher_factory(key=individual).decipher(cipher_text) for individual in population]
            text_scores = [self.score_function.score(text) for text in texts]
            toc = time.time_ns()

            # Best candidate for this step:
            best_index = np.argmax(text_scores)

            # Dispatch step information:
            yield {
                "attack_id": attack_id,
                "step_index": step_index,
                "max_steps": max_steps,
                "min_score": np.min(text_scores),
                "max_score": np.max(text_scores),
                "scoring_time": (toc - tic)/1e9,
                "best_key": population[best_index],
                "best_text": texts[best_index]
            }

            # Stop criterion:

            # Create new generation:

            pass


def main():

    import pathlib

    def hamming(x, key):
        if len(x) == len(key):
            return distance.hamming(list(x), list(key)) * len(x)

    paths = list(sorted(pathlib.Path("pysgrs/resources/texts/fr").glob("*.txt")))

    counter = 0

    solutions = []
    for weights in [
        [0.6, 0.3, 0.1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]:

        score = scores.MixedNGramScore(weights=weights)
        breaker = VigenereGeneticAlgorithmBreaker_v1(score)

        for path in paths:

            # Load text:
            text = path.read_text("utf-8")
            print(path)

            # Strip accents:
            text = AsciiCleaner.strip_accents(text)

            # Target:
            target = score.score(text)

            for key in ["SECRET", "SECRETTOKEN", "GENETICALGORITHM", "THECOLLATZCONJECTURE", "ABCDEFGHIJKLMNOPQRSTUZVWXYZ"]:

                # Cipher text:
                cipher = VigenereCipher(key=key)
                cipher_text = cipher.encipher(text)

                for seed in [123456789, 987654321, 546987123]:

                    for mutation_threshold in [0.5, 0.80, 0.99]:

                        for population_size in [10, 50, 100, 500, 1000]:

                            # Attack cipher text:
                            # generations = list(
                            #     breaker.attack_with_key_size_guess(
                            #         cipher_text, min_key_size=10, max_key_size=30, order_by="mean", max_guess=4,
                            #         population_size=population_size, generation_count=50,
                            #         mutation_threshold=mutation_threshold, seed=seed
                            #     )
                            # )

                            generations = list(
                                breaker.attack(
                                    cipher_text, key_size=len(key),
                                    population_size=population_size, generation_count=50,
                                    threshold=mutation_threshold, seed=seed,
                                    exact_key=key
                                )
                            )

                            counter += 1
                            frame = pd.DataFrame(generations)
                            frame["hamming_distance"] = frame["best_key"].apply(hamming, args=(key,))
                            filename = "media/break_vigenere_{}.xlsx".format(counter)
                            frame = frame.assign(
                                weights=str(weights), setup=counter, target=target, original_key=key,
                                text_length=len(text), path=str(path), dump=filename
                            )
                            frame.to_excel(filename)
                            solutions.append(frame)

        #                     break
        #                 break
        #             break
        #         break
        #     break
        # break

    # Dump results:
    solutions = pd.concat(solutions)
    print(solutions)
    solutions.to_excel("media/break_vigenere_all.xlsx")


if __name__ == "__main__":
    main()
