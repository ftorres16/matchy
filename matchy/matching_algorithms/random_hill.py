import numpy as np

from matchy.matching_algorithms.base_matching_class import BaseMatchingClass
from matchy.matching_algorithms.hill_climbing import HillClimbing


class RandomHill(BaseMatchingClass):
    """
    Try to optimize by using hill climbing on N randomly chosen matrixes.
    """

    def __init__(self, mat, num_matrixes=100, *args, **kwargs):
        super().__init__(mat, *args, **kwargs)

        random_matrixes = np.empty(shape=(num_matrixes, *mat.shape), dtype=mat.dtype)

        for index in range(num_matrixes):
            random_mat = np.copy(mat)
            flat_mat = random_mat.ravel()
            np.random.shuffle(flat_mat)
            random_matrixes[index] = flat_mat.reshape(mat.shape)

        self.candidates = [
            HillClimbing(random_mat)
            for random_mat in np.unique(random_matrixes, axis=0)
        ]

    def _optimize(self):
        for candidate in self.candidates:
            if not candidate.reached_optimal:
                candidate._optimize()

                if candidate.error < self.error:
                    self.mat = candidate.mat
                    self.error = candidate.error

                return

        self.reached_optimal = True
