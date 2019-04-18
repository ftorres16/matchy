import string

import click

from matchy.matching_functions import match, METHODS


MAX_DEVICES = 26
MAX_M = 30


@click.command()
@click.option(
    "-n",
    type=click.IntRange(1, MAX_DEVICES),
    help="Number of different devices to be matched.",
    prompt="Number of devices",
)
@click.option(
    "-m",
    type=click.IntRange(1, MAX_M),
    multiple=True,
    help="Multiplicity of each device.",
)
@click.option(
    "--method",
    help="Method to find the optimal matrix.",
    type=click.Choice(METHODS.keys()),
    default="random",
)
def cli(n, m, method):
    """
    Matching for IC devices.

    Usage:
    `matchy -n 3 -m 2 -m 3 -m 1`

    This will match 3 devices, the first of which has m=2, the second has m=3, the third has m=1.
    """

    if len(m) != n:
        # Multiplicities mismatch N. Enter them manually.
        m = tuple(
            [
                click.prompt(
                    f"Multiplicity for device {string.ascii_uppercase[i]}",
                    type=click.IntRange(1, MAX_M),
                )
                for i in range(n)
            ]
        )

    click.echo(match(n, m, method))
