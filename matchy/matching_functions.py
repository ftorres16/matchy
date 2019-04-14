import math
import string

import numpy as np

MAX_TRIES = 10000
TOL = 1e-6


def match(n, m):
    """
    Returns a matrix with the best possible matching for N devices,
    where there multiplicities are given by the elements in M.
    """
    # get a list where each member is a piece of each device
    flattened_names = [string.ascii_uppercase[i] for i in range(n) for _ in range(m[i])]

    # get the lenght of the square where the devices will be laid
    L = math.ceil(math.sqrt(len(flattened_names)))

    # add spare devices as needed
    n_spares = L ** 2 - len(flattened_names)
    flattened_names += ["?"] * n_spares

    match_matrix = np.array(flattened_names).reshape(L, L)

    # introduce some randomness to make it faster
    match_matrix = match_matrix.ravel()
    np.random.shuffle(match_matrix)
    match_matrix = match_matrix.reshape(L, L)

    error = get_error(match_matrix)
    num_tries = 0
    random_matrix = np.copy(match_matrix)
    while error > TOL and num_tries < MAX_TRIES:
        # random search
        random_matrix = random_matrix.ravel()
        np.random.shuffle(random_matrix)
        random_matrix = random_matrix.reshape(L, L)

        if get_error(random_matrix) < error:
            match_matrix = np.copy(random_matrix)

        num_tries += 1

    return match_matrix


def get_error(mat, dummy_name="?"):
    """
    Returns the root of the square sum of the centroids for all the elements
    in `mat` while ignoring the dummies.
    """
    names = np.unique(mat)
    names = names[names != dummy_name]

    centroids = np.zeros((len(names), 2))

    for index, name in enumerate(names):
        row_vals, col_vals = np.where(mat == name)
        center_y = np.mean(row_vals) - (len(row_vals) - 1) / 2
        center_x = np.mean(col_vals) - (len(col_vals) - 1) / 2
        centroids[index] = center_x, center_y

    return np.sqrt(np.sum(centroids ** 2))
