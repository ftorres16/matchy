import math
import string

import numpy as np

from matchy.matching_algorithms.random_search import random_search
from matchy.matching_algorithms.hill_climbing import hill_climbing


MAX_TRIES = 100000
TOL = 1e-6

METHODS = {"random": random_search, "hill_climbing": hill_climbing}


def match(n, m, method="random"):
    """
    Returns a matrix with the best possible matching for N devices,
    where there multiplicities are given by the elements in M.
    """
    # get all possible names
    names = [string.ascii_uppercase[i] for i in range(n)]
    # get a list where each member is a piece of each device
    flattened_names = [
        name for index, name in enumerate(names) for _ in range(m[index])
    ]

    # get the lenght of the square where the devices will be laid
    L = math.ceil(math.sqrt(len(flattened_names)))

    # add spare devices as needed
    n_spares = L ** 2 - len(flattened_names)
    flattened_names += ["?"] * n_spares

    match_matrix = np.array(flattened_names)

    # introduce some randomness to make it faster
    np.random.shuffle(match_matrix)
    match_matrix = match_matrix.reshape(L, L)

    match_matrix = METHODS[method](match_matrix, names=names)

    return match_matrix
