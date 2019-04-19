from helper_functions import get_error


TOL = 1e-6
MAX_TRIES = 100_000


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
