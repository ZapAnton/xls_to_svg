from xls_to_svg.cli import parse_cli_arguments, handle_arguments


if __name__ == '__main__':
    cli_arguments = parse_cli_arguments()
    handle_arguments(cli_arguments)
