import numpy as np

from matchy.helper_functions import get_error
from matchy.matching_algorithms.base_matching_class import BaseMatchingClass


class HillClimbing(BaseMatchingClass):
    """
    Try to optimize the matrix by performing simple hill climbing.
    This means, swapping devices one place at a time.
    """

    def _optimize(self):
        if self.reached_optimal:
            return

        rows, cols = self.mat.shape

        for y, x in np.ndindex(*self.mat.shape):
            # get all the directions in which the target component will be swapped
            swap_dirs = []
            if x != cols - 1:
                swap_dirs.append((1, 0))
            if y != rows - 1:
                swap_dirs.append((0, 1))
            if x != cols - 1 and y != rows - 1:
                swap_dirs.append((1, 1))
            if x != 0 and y != rows - 1:
                swap_dirs.append((-1, 1))

            for swap_dir in swap_dirs:
                if self.swap_components((x, y), swap_dir):
                    return

        self.reached_optimal = True

    def swap_components(self, swap_point, swap_dir):
        """
        Given a matrix `self.mat`, this function will check if the error improves or decreases by
        swapping element `swap point` in (x, y) format with the one that's offset one `swap_dir`.

        This function will return `True` if the matrix with the swapped components if the error
        diminishes and `False` if it doesn't.

        For example, if `self.mat` is [['A', 'B'],
                                       ['A', 'B']]

            - `swap_point` (0,0) and `swap_dir` (0,1) it returns `True` and `self.mat` will be
                [['B', 'A'],
                 ['A', 'B']]

            - `swap_point` (0,0) and `swap_dir` (1,1) it returns `False` and `self.mat` will be
                [['A', 'B'],
                 ['A', 'B']]
        """
        x, y = swap_point
        swap_x, swap_y = swap_dir

        if self.mat[y, x] == self.mat[y + swap_y, x + swap_x]:
            # no point in swapping identical devices
            return False

        self.mat[(y, y + swap_y), (x, x + swap_x)] = self.mat[
            (y + swap_y, y), (x + swap_x, x)
        ]

        new_error = get_error(self.mat, names=self.names, dummy_name=self.dummy_name)

        if new_error < self.error:
            self.error = new_error
            return True
        else:
            # undo the swap
            self.mat[(y, y + swap_y), (x, x + swap_x)] = self.mat[
                (y + swap_y, y), (x + swap_x, x)
            ]
            return False
