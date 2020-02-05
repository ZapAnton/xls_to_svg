import argparse
from pathlib import Path
from xls_to_svg.chart_plotter import ChartPlotter


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Convert XLS tables into SVG charts')
    parser.add_argument('-l',
                        '--list-chart-types',
                        action='store_true',
                        dest='show_chart_types',
                        help='display all available chart types')
    parser.add_argument('-t',
                        '--chart-type',
                        action='store',
                        dest='chosen_chart_type',
                        help='sets output chart type')
    parser.add_argument('xls_filepath',
                        type=Path,
                        action='store',
                        help='path to the input XLS file',
                        nargs='?')
    arguments = parser.parse_args()
    return arguments


def handle_arguments(arguments: argparse.Namespace):
    if arguments.show_chart_types:
        output: str = '\n'.join(ChartPlotter.CHART_TYPES)
        print(output)
        return
    if not arguments.chosen_chart_type in ChartPlotter.CHART_TYPES:
        print(
            f'Chosen chart type "{arguments.chosen_chart_type}" does not exist. Aborting'
        )
        return
    if not arguments.xls_filepath:
        print('No input XLS file path provided. Aborting')
        return
    if not arguments.xls_filepath.exists():
        print(
            f'Input XLS file path "{arguments.xls_filepath}" does not exist. Aborting'
        )
        return
    plotter = ChartPlotter(arguments.chosen_chart_type, arguments.xls_filepath)
    plotter.plot()
