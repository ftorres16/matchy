import string

import click

from matchy.matching_functions import match, report, METHODS


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

    click.echo("\n")
    matched_matrix = match(n, m, method)
    click.echo(matched_matrix)
    click.echo("\n")

    matching_report = report(matched_matrix)

    # pretty print the report as a table
    col_width = max([len(header) for header in matching_report.keys()])
    num_cols = len(matching_report.keys())
    click.echo("┌" + "─┬─".join(["─" * col_width for _ in range(num_cols)]) + "┐")
    click.echo(
        "│"
        + " │ ".join([f"{header:>{col_width}}" for header in matching_report.keys()])
        + "│"
    )
    click.echo("├" + "─┼─".join(["─" * col_width for _ in range(num_cols)]) + "┤")

    for index, name in enumerate(matching_report["names"]):
        centroid_x = f"{matching_report['centroid_x'][index]: .3}"
        centroid_y = f"{matching_report['centroid_y'][index]: .3}"
        error = f"{matching_report['error'][index]: .3}"

        if index != 0:
            click.echo(
                "├" + "┈┼┈".join(["┈" * col_width for _ in range(num_cols)]) + "┤"
            )

        click.echo(
            "│"
            + " │ ".join(
                [
                    f"{value:>{col_width}}"
                    for value in (name, centroid_x, centroid_y, error)
                ]
            )
            + "│"
        )

    click.echo("└" + "─┴─".join(["─" * col_width for _ in range(num_cols)]) + "┘")
    click.echo("\n")
