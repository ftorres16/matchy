import math
import string

import numpy as np


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

    match_matrix = np.array(flattened_names).reshape((L, L))

    return match_matrix
