from matchy.matching_algorithms.base_matching_class import BaseMatchingClass


class DoNothing(BaseMatchingClass):
    """
    Perform no changes on the matrix. Can be useful for testing.
    """

    def _optimize(self):
        self.reached_optimal = True
