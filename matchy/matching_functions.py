import math
import string

import numpy as np

from matchy.matching_algorithms.random_search import RandomSearch
from matchy.matching_algorithms.hill_climbing import HillClimbing
from matchy.helper_functions import get_centroids, get_device_names


METHODS = {"random": RandomSearch, "hill_climbing": HillClimbing}


def match(n=None, m=None, method="random", initial_guess=None):
    """
    Returns a matrix with the best possible matching for N devices,
    where there multiplicities are given by the elements in M.

    Optionally, you can pass an initial guess matrix that will attempt
    to be matched. In this case, M and N are ignored.
    """
    if initial_guess is not None:
        match_matrix = initial_guess
        names = get_device_names(match_matrix)
    else:
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

    matching_method = METHODS[method](match_matrix)
    matching_method.run()

    return matching_method.mat


def report(mat):
    names = get_device_names(mat)
    centroids = get_centroids(mat, names=names)
    errors = np.sqrt(np.sum(np.square(centroids), axis=1))

    return {
        "names": names,
        "centroid_x": centroids[:, 0],
        "centroid_y": centroids[:, 1],
        "error": errors
    }
