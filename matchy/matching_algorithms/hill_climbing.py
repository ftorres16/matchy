from matchy.helper_functions import get_error


TOL = 1e-6
MAX_TRIES = 100_000


def hill_climbing(match_matrix, names=None, dummy_name="?"):
    """
    Try to optimize the matrix by performing simple hill climbing.
    This means, swapping devices one place at a time.
    """
    error = get_error(match_matrix, names=names, dummy_name=dummy_name)

    rows, cols = match_matrix.shape

    for _ in range(MAX_TRIES):
        if error < TOL:
            break

        break_flag = False

        for x in range(cols):
            for y in range(rows):
                # get all the directions in which the target component will be swapped
                swap_dirs = []
                if x != cols - 1:
                    swap_dirs.append((1, 0))
                if y != rows - 1:
                    swap_dirs.append((0, 1))
                if x != cols - 1 and y != rows - 1:
                    swap_dirs.append((1, 1))
                if x != 0 and y != rows - 1:
                    swap_dirs.append((-1, 1))

                for swap_dir in swap_dirs:
                    match_matrix, error, break_flag = swap_components(
                        match_matrix, (x, y), swap_dir, names, dummy_name, error
                    )
                    if break_flag:
                        break

                if break_flag:
                    break

            if break_flag:
                break
        else:
            break

    return match_matrix


def swap_components(mat, swap_point, swap_dir, names, dummy_name, error):
    """
    Given a matrix `mat`, this function will check if the error improves or decreases by
    swapping element `swap point` in (x, y) format with the one that's offset one `swap_dir`.

    This function will return the matrix with the swapped components if the error diminishes
    and the old matrix if it doesn't.

    For example, if `mat` is [['A', 'B'],
                              ['A', 'B']]

        - `swap_point` (0,0) and `swap_dir` (0,1) returns
            [['B', 'A'],
             ['A', 'B']]

        - `swap_point` (0,0) and `swap_dir` (1,1) returns
            [['A', 'B'],
             ['A', 'B']]
    """
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
