# matchy

A tool for matching devices in analog layout in a streamlined and automated way.

## Installation

Run `pip install matchy` for the latest stable version.

### Development

1. Git clone [this repository](https://github.com/ftorres16/matchy/).
2. `cd` to the root folder where this repo is cloned.
3. `poetry install` to install it with [Python Poetry](https://python-poetry.org/).

## Usage

1. Write `matchy` in a terminal.
2. The CLI will ask you for the number of devices you want to match.
3. The CLI will ask you for the multiplicity of each device.
4. Sit back and wait for the optimization to occur.
5. You will be prompted with the system's best guess for the optimal matrix, as well as some key metrics, such as the centroid of each device and total error.

You may want to use `matchy` only to calculate the centroid of your devices. In that case:

1. Save your device matrix configuration in a CSV file.
2. Run `matchy --initial <PATH> --method do_nothing`
3. Matchy will print the centroid for each device in a table.
