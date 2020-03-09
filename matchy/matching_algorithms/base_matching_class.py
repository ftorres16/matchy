from matchy.helper_functions import get_device_names, get_error


class BaseMatchingClass:
    def __init__(self, mat, dummy_name="?", tol=1e-3, max_tries=10_000):
        self.mat = mat
        self.dummy_name = dummy_name
        self.names = get_device_names(mat, dummy_name=dummy_name)
        self.error = get_error(mat, names=self.names)

        self.tol = tol
        self.max_tries = max_tries
        self.reached_optimal = False

    def run(self):
        """
        Performs the matching iterator until the optimal is reached or `self.max_tries` is exceeded.
        """
        for _ in self._iter():
            return

    def _iter(self):
        """
        Iterator to find the optimal matrix.
        This function is provided for front end implementation of progress bars.
        """
        for _ in range(self.max_tries):
            if self.error < self.tol or self.reached_optimal:
                break
            else:
                self._optimize()
                yield

    def _optimize():
        """
        Perform one iteration of the optimizer.

        Returns True when the optimal is reached, false if more iterations are needed.
        """
        raise NotImplementedError("Please reimplement this in your custom matching class.")
