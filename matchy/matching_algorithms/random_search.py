import numpy as np

from matchy.helper_functions import get_error


TOL = 1e-6
MAX_TRIES = 100_000


def random_search(match_matrix, names=None, dummy_name="?"):
    """
    Try to optimize the matrix by performing a random search.
    """
    error = get_error(match_matrix, names=names, dummy_name=dummy_name)
    num_tries = 0
    random_matrix = np.copy(match_matrix)

    while error > TOL and num_tries < MAX_TRIES:
        random_matrix = random_matrix.ravel()
        np.random.shuffle(random_matrix)
        random_matrix = random_matrix.reshape(match_matrix.shape)

        new_error = get_error(random_matrix, names=names, dummy_name=dummy_name)
        if new_error < error:
            error = new_error
            match_matrix = np.copy(random_matrix)

        num_tries += 1

    return match_matrix
