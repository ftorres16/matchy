import numpy as np

from matchy.helper_functions import get_error
from matchy.matching_algorithms.base_matching_class import BaseMatchingClass


class RandomSearch(BaseMatchingClass):
    """
    Try to optimize the matrix by performing a random search.
    """

    def optimize(self):
        random_matrix = np.copy(self.mat)

        for _ in range(self.max_tries):
            if self.error < self.tol:
                break

            random_matrix = random_matrix.ravel()
            np.random.shuffle(random_matrix)
            random_matrix = random_matrix.reshape(self.mat.shape)

            new_error = get_error(random_matrix, names=self.names, dummy_name=self.dummy_name)
            if new_error < self.error:
                self.error = new_error
                self.mat = np.copy(random_matrix)

        return
