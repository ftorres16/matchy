from matchy.helper_functions import get_device_names, get_error


class BaseMatchingClass:
    def __init__(self, mat, dummy_name="?", tol=1e-3, max_tries=1_000):
        self.mat = mat
        self.dummy_name = dummy_name
        self.names = get_device_names(mat, dummy_name=dummy_name)
        self.error = get_error(mat, names=self.names)

        self.tol = tol
        self.max_tries = max_tries

    def optimize():
        raise NotImplementedError("Please reimplement this in your custom matching class.")
