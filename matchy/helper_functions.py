import numpy as np


def get_device_names(mat, dummy_name="?"):
    names = np.unique(mat)
    return names[names != dummy_name]


def get_centroids(mat, names=None, dummy_name="?"):
    """
    Returns the centroid for each device in matrix `mat` in (x,y) format.
    The coordinates are so that (0,0) is at the center of `mat`.

    `names` lets you pass all the named devices to avoid running through `mat` too many times.
    `dummy_name` lets you ignore a specific device.
    """
    if names is None:
        names = get_device_names(mat, dummy_name=dummy_name)

    centroids = np.array(
        [np.mean(np.where(mat == name), axis=1)[::-1] for name in names]
    )

    # Re-center the centroids so the origin is at the center of `mat` and not at its corner.
    offset = (np.array(mat.shape[::-1]) - 1) / 2
    centroids -= offset

    # Flip y axis to be more intuitive
    centroids[:, 1] *= -1

    return centroids


def get_error(mat, centroids=None, names=None, dummy_name="?"):
    """
    Returns the root square sum of the centroids for all the elements
    in `mat` while ignoring the dummies.
    """
    if centroids is None:
        centroids = get_centroids(mat, names, dummy_name)

    return np.linalg.norm(centroids)


def get_report(mat):
    """
    Get a report of the error and centroids of all devices in a matrix.
    """
    names = get_device_names(mat)
    centroids = get_centroids(mat, names=names)
    errors = np.linalg.norm(centroids, axis=1)

    # add total error to the report
    names = np.append(names, 'total')
    centroids = np.append(centroids, [[np.nan, np.nan]], axis=0)
    errors = np.append(errors, np.linalg.norm(errors))

    return {
        "names": names,
        "centroid_x": centroids[:, 0],
        "centroid_y": centroids[:, 1],
        "error": errors
    }
