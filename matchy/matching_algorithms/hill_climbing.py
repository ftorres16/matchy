from matchy.helper_functions import get_error


TOL = 1e-6
MAX_TRIES = 100_000


def hill_climbing(match_matrix, names=None, dummy_name="?"):
    """
    Try to optimize the matrix by performing simple hill climbing.
    This means, moving devices one place at a time.
    """
    error = get_error(match_matrix, names=names, dummy_name=dummy_name)

    rows, cols = match_matrix.shape

    for _ in range(MAX_TRIES):
        if error < TOL:
            break

        break_flag = False

        for x in range(cols):
            for y in range(rows):
                if x != cols - 1:
                    # horizontal swap
                    match_matrix, error, break_flag = swap_components(
                        match_matrix, (x, y), (1, 0), names, dummy_name, error
                    )
                    if break_flag:
                        break

                if y != rows - 1:
                    # vertical swap
                    match_matrix, error, break_flag = swap_components(
                        match_matrix, (x, y), (0, 1), names, dummy_name, error
                    )
                    if break_flag:
                        break

                if x != cols - 1 and y != rows - 1:
                    # diagonal swap
                    match_matrix, error, break_flag = swap_components(
                        match_matrix, (x, y), (1, 1), names, dummy_name, error
                    )
                    if break_flag:
                        break

                if x != 0 and y != rows - 1:
                    # diagonal swap
                    match_matrix, error, break_flag = swap_components(
                        match_matrix, (x, y), (-1, 1), names, dummy_name, error
                    )
                    if break_flag:
                        break

            if break_flag:
                break
        else:
            break

    return match_matrix


def swap_components(mat, swap_point, swap_dir, names, dummy_name, error):
    x = swap_point[0]
    y = swap_point[1]
    swap_x = swap_dir[0]
    swap_y = swap_dir[1]

    mat[(y, y + swap_y), (x, x + swap_x)] = mat[(y + swap_y, y), (x + swap_x, x)]

    new_error = get_error(mat, names=names, dummy_name=dummy_name)

    if new_error < error:
        error = new_error
        return mat, error, True

    # undo the swap
    mat[(y, y + swap_y), (x, x + swap_x)] = mat[(y + swap_y, y), (x + swap_x, x)]
    return mat, error, False
