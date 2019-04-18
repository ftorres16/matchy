import math
import string

import numpy as np

MAX_TRIES = 100000
TOL = 1e-6


def match(n, m, method="random"):
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

    match_matrix = METHODS[method](match_matrix)

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
        center_y = np.mean(row_vals) - (mat.shape[0] - 1) / 2
        center_x = np.mean(col_vals) - (mat.shape[1] - 1) / 2
        centroids[index] = center_x, center_y

    return np.sqrt(np.sum(centroids ** 2))


def random_search(match_matrix):
    """
    Try to optimize the matrix by performing a random search.
    """
    error = get_error(match_matrix)
    num_tries = 0
    random_matrix = np.copy(match_matrix)

    while error > TOL and num_tries < MAX_TRIES:
        random_matrix = random_matrix.ravel()
        np.random.shuffle(random_matrix)
        random_matrix = random_matrix.reshape(match_matrix.shape)

        new_error = get_error(random_matrix)
        if new_error < error:
            error = new_error
            match_matrix = np.copy(random_matrix)

        num_tries += 1

    return match_matrix


def simple_hill_climbing(match_matrix):
    """
    Try to optimize the matrix by performing simple hill climbing.
    This means, moving devices one place at a time.
    """
    error = get_error(match_matrix)

    rows, cols = match_matrix.shape

    for _ in range(MAX_TRIES):
        if error < TOL:
            break

        break_flag = False

        for x in range(cols):
            for y in range(rows):
                if x != cols - 1:
                    # horizontal swap
                    match_matrix[(y, y), (x, x + 1)] = match_matrix[(y, y), (x + 1, x)]

                    new_error = get_error(match_matrix)
                    if new_error < error:
                        error = new_error
                        break_flag = True
                        break

                    # undo the horizontal swap
                    match_matrix[(y, y), (x, x + 1)] = match_matrix[(y, y), (x + 1, x)]

                if y != rows - 1:
                    # vertical swap
                    match_matrix[(y, y + 1), (x, x)] = match_matrix[(y + 1, y), (x, x)]

                    new_error = get_error(match_matrix)
                    if new_error < error:
                        error = new_error
                        break_flag = True
                        break

                    # undo the vertical swap
                    match_matrix[(y, y + 1), (x, x)] = match_matrix[(y + 1, y), (x, x)]

                if x != cols - 1 and y != rows - 1:
                    # diagonal swap
                    match_matrix[(y, y + 1), (x, x + 1)] = match_matrix[
                        (y + 1, y), (x + 1, x)
                    ]

                    new_error = get_error(match_matrix)
                    if new_error < error:
                        error = new_error
                        break_flag = True
                        break

                    # diagonal swap
                    match_matrix[(y, y + 1), (x, x + 1)] = match_matrix[
                        (y + 1, y), (x + 1, x)
                    ]

                if x != 0 and y != rows - 1:
                    # diagonal swap
                    match_matrix[(y, y + 1), (x, x - 1)] = match_matrix[
                        (y + 1, y), (x - 1, x)
                    ]

                    new_error = get_error(match_matrix)
                    if new_error < error:
                        error = new_error
                        break_flag = True
                        break

                    # diagonal swap
                    match_matrix[(y, y + 1), (x, x - 1)] = match_matrix[
                        (y + 1, y), (x - 1, x)
                    ]

            if break_flag:
                break
        else:
            break

    return match_matrix


METHODS = {"random": random_search, "hill_climbing": simple_hill_climbing}
