import numpy as np

from matchy.matching_algorithms.base_matching_class import BaseMatchingClass
from matchy.matching_algorithms.hill_climbing import HillClimbing


class RandomHill(BaseMatchingClass):
    """
    Try to optimize by using hill climbing on N randomly chosen matrixes.
    """

    def __init__(self, mat, num_matrixes=100, *args, **kwargs):
        super().__init__(mat, *args, **kwargs)

        random_matrixes = []
        for _ in range(num_matrixes):
            random_mat = np.copy(mat)
            flat_mat = random_mat.ravel()
            np.random.shuffle(flat_mat)
            random_matrixes.append(flat_mat.reshape(mat.shape))

        self.candidates = [
            {"optimizer": HillClimbing(random_mat), "reached_optimal": False}
            for random_mat in random_matrixes
        ]

    def _optimize(self):
        for candidate in self.candidates:
            if not candidate["reached_optimal"]:
                candidate["reached_optimal"] = candidate["optimizer"]._optimize()

                if candidate["optimizer"].error < self.error:
                    self.mat = candidate["optimizer"].mat
                    self.error = candidate["optimizer"].error

                return False

        return True
