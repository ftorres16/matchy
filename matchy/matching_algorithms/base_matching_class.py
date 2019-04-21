from matchy.helper_functions import get_device_names, get_error


class BaseMatchingClass:
    def __init__(self, mat, dummy_name="?", tol=1e-3, max_tries=10_000):
        self.mat = mat
        self.dummy_name = dummy_name
        self.names = get_device_names(mat, dummy_name=dummy_name)
        self.error = get_error(mat, names=self.names)

        self.tol = tol
        self.max_tries = max_tries

    def run(self):
        for _ in range(self.max_tries):
            if self.error < self.tol:
                return

            reached_optimal = self._optimize()
            if reached_optimal:
                return

    def _optimize():
        """
        Returns True when the optimal is reached, false if more iterations are needed.
        """
        raise NotImplementedError("Please reimplement this in your custom matching class.")
