from cli import parse_cli_arguments, handle_arguments


def main():
    cli_arguments = parse_cli_arguments()
    handle_arguments(cli_arguments)


if __name__ == '__main__':
    main()
