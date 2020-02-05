import argparse


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
    parser.add_argument(
        'xls_filepath',
        action='store',
        help='path to the input XLS file',
    )
    arguments = parser.parse_args()
    return arguments
