import numpy as np


def get_device_names(mat, dummy_name="?"):
    names = np.unique(mat)
    return names[names != dummy_name]


def get_centroids(mat, names=None, dummy_name="?"):
    """
    Get the centroid for each device in matrix `mat`.
    The coordinates are so that (0,0) is at the center of `mat`.

    `names` lets you pass all the named devices to avoid running through `mat` too many times.
    `dummy_name` lets you ignore a specific device.
    """
    if names is None:
        names = get_device_names(mat, dummy_name)

    centroids = np.zeros((names.shape[0][0], 2))

    for index, name in enumerate(names):
        row_vals, col_vals = np.where(mat == name)
        center_y = np.mean(row_vals) - (mat.shape[0] - 1) / 2
        center_x = np.mean(row_vals) - (mat.shape[1] - 1) / 2
        centroids[index] = center_x, center_y

    return centroids


def get_error(mat, centroids=None, names=None, dummy_name="?"):
    """
    Returns the root square sum of the centroids for all the elements
    in `mat` while ignoring the dummies.
    """
    if centroids is None:
        centroids = get_centroids(mat, names, dummy_name)

    return np.sqrt(np.sum(np.square(centroids)))
