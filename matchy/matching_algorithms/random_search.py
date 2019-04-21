import numpy as np

from matchy.helper_functions import get_error
from matchy.matching_algorithms.base_matching_class import BaseMatchingClass


class RandomSearch(BaseMatchingClass):
    """
    Try to optimize the matrix by performing a random search.
    """

    def __init__(self, mat, *args, **kwargs):
        super().__init__(mat, *args, **kwargs)
        self.random_matrix = np.copy(mat)

    def _optimize(self):
        self.random_matrix = self.random_matrix.ravel()
        np.random.shuffle(self.random_matrix)
        self.random_matrix = self.random_matrix.reshape(self.mat.shape)

        new_error = get_error(self.random_matrix, names=self.names, dummy_name=self.dummy_name)
        if new_error < self.error:
            self.error = new_error
            self.mat = np.copy(self.random_matrix)

        return False
