import click


def pretty_print_matrix(mat):
    """
    Pretty print a 2D numpy array.

    For example, if `mat` is [['A', 'B'],
                              ['B', 'A']]

    Then the output will print:
        ┌─────┐
        │ A B │
        │ B A │
        └─────┘
    """
    box_top = "─" * (2 * mat.shape[1] + 1)
    click.echo(f"┌{box_top}┐")
    for row in mat:
        devices = " ".join(row)
        click.echo(f"│ {devices} │")
    click.echo(f"└{box_top}┘")


def pretty_print_table(headers, rows):
    """
    Pretty print a table with headers and its rows.

    `headers` should be a list of strings.
    `rows` should be a list of lists of strings each one with the same len as `headers`.

    For example, if `headers = ['col1', 'col2']` and `rows = [['row1', 'val1'], ['row2', 'val2']]`

    Then the output will print:
        ┌──────┬──────┐
        │ col1 │ col2 │
        ├──────┼──────┤
        │ row1 │ val1 │
        ├┈┈─┈┈┈┼┈┈┈┈┈┈┤
        │ row2 │ val2 │
        └──────┴──────┘
    """
    col_width = len(max(headers, key=len))
    num_cols = len(headers)

    box_top = "─┬─".join(["─" * col_width for _ in range(num_cols)])
    headers_line = " │ ".join([f"{header:>{col_width}}" for header in headers])
    separator = "─┼─".join(["─" * col_width for _ in range(num_cols)])
    row_separator = "┈┼┈".join(["┈" * col_width for _ in range(num_cols)])
    box_bot = "─┴─".join(["─" * col_width for _ in range(num_cols)])

    click.echo(f"┌─{box_top}─┐")
    click.echo(f"│ {headers_line} │")
    click.echo(f"├─{separator}─┤")

    for index, row in enumerate(rows):
        if index > 0:
            click.echo(f"├┈{row_separator}┈┤")

        row = " │ ".join([f"{value:>{col_width}}" for value in row])
        click.echo(f"│ {row} │")

    click.echo(f"└─{box_bot}─┘")
