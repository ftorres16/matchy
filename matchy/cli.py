import string

import click
import numpy as np

from matchy.helper_functions import get_report, get_device_names
from matchy.matching_algorithms.random_search import RandomSearch
from matchy.matching_algorithms.hill_climbing import HillClimbing
from matchy.matching_algorithms.random_hill import RandomHill
from matchy.matching_algorithms.do_nothing import DoNothing
from matchy.pretty_print import pretty_print_matrix, pretty_print_table


MAX_DEVICES = 26
MAX_M = 30
METHODS = {
    "random": RandomSearch,
    "hill_climbing": HillClimbing,
    "random_hill": RandomHill,
    "do_nothing": DoNothing,
}


@click.command()
@click.option(
    "-n",
    type=click.IntRange(1, MAX_DEVICES),
    help="Number of different devices to be matched.",
)
@click.option(
    "-m",
    type=click.IntRange(1, MAX_M),
    multiple=True,
    help="Multiplicity of each device.",
)
@click.option(
    "--mat_height",
    type=click.IntRange(1, MAX_DEVICES * MAX_M),
    help="Height for the final matching matrix",
)
@click.option(
    "--mat_width",
    type=click.IntRange(1, MAX_DEVICES * MAX_M),
    help="Width for the final matching matrix",
)
@click.option(
    "--method",
    help="Method to find the optimal matrix.",
    type=click.Choice(METHODS.keys()),
    default="random_hill",
)
@click.option(
    "--initial", help="File to load the initial matrix guess.", type=click.Path()
)
@click.option("--output", help="File to save the resulting matrix.", type=click.Path())
def cli(n, m, method, mat_height, mat_width, initial, output):
    """
    Matching for IC devices.

    Usage:
    `matchy -n 3 -m 2 -m 3 -m 1`

    This will match 3 devices, the first of which has m=2, the second has m=3, the third has m=1.
    """

    if initial:
        match_matrix = np.genfromtxt(initial, dtype="<U1", delimiter=",")
        names = get_device_names(match_matrix)
    else:
        if not n:
            n = click.prompt("Number of devices", type=click.IntRange(1, MAX_DEVICES))
        # If multiplicities mismatch N. Enter them manually.
        names = [string.ascii_uppercase[i] for i in range(n)]
        if len(m) != n:
            m = [
                click.prompt(
                    f"Multiplicity for device {name}", type=click.IntRange(1, MAX_M)
                )
                for name in names
            ]
            m = tuple(m)

        # get a list where each member is a piece of each device
        flattened_names = [name for i, name in enumerate(names) for _ in range(m[i])]
        num_devices = len(flattened_names)

        mat_height = mat_height or 0
        mat_width = mat_width or 0

        click.echo("")
        if mat_height * mat_width >= num_devices:
            pass
        elif click.confirm(
            "Would you like to manually enter matrix dimensions? (defaults to square)"
        ):
            while mat_height * mat_width < num_devices:
                if mat_height * mat_width != 0:
                    # this means that height and width were given by the user at least once
                    click.echo(
                        "Dimensions entered are too small. Please enter valid matrix dimensions"
                    )
                mat_height = click.prompt(
                    "Matrix height", type=click.IntRange(1, num_devices)
                )
                mat_width = click.prompt(
                    "Matrix width", type=click.IntRange(1, num_devices)
                )
        else:
            # defaults to a square
            mat_height = int(np.ceil(np.sqrt(num_devices)))
            mat_width = int(np.ceil(np.sqrt(num_devices)))

        # add spare devices as needed
        n_spares = mat_height * mat_width - num_devices
        flattened_names += ["?"] * n_spares

        match_matrix = np.array(flattened_names)

        # introduce some randomness to make it faster
        np.random.shuffle(match_matrix)
        match_matrix = match_matrix.reshape(mat_height, mat_width)

    optimizer = METHODS[method](match_matrix)

    # The actual optimization is performed here.
    click.echo()
    with click.progressbar(optimizer._iter(), length=optimizer.max_tries) as bar:
        for _ in bar:
            pass

    matched_matrix = optimizer.mat

    # pretty print the matrix in a box
    click.echo()
    pretty_print_matrix(matched_matrix)
    click.echo()

    matching_report = get_report(matched_matrix)

    # pretty print the report as a table
    headers = matching_report.keys()
    rows = [
        [
            name,
            f"{matching_report['centroid_x'][index]: .3}",
            f"{matching_report['centroid_y'][index]: .3}",
            f"{matching_report['error'][index]: .3}",
        ]
        for index, name in enumerate(matching_report["names"])
    ]
    pretty_print_table(headers, rows)
    click.echo()

    if output is None:
        if click.confirm("Would you like to save the matrix to a .csv file?"):
            output = click.prompt(
                "Enter path to file to save the matrix", type=click.Path()
            )

    if output is not None:
        np.savetxt(output, matched_matrix, fmt="%s", delimiter=",")
