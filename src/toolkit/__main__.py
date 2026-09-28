import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def main() -> None:
    """Обрабатывает аргументы командной строки и запускает нужную команду"""
    parser = argparse.ArgumentParser(description="Консольный калькулятор и конвертер величин")
    subparsers = parser.add_subparsers(dest="command")

    calc_parser = subparsers.add_parser("calc", help="Вычислить математическое выражение")
    calc_parser.add_argument("expression")

    convert_parser = subparsers.add_parser("convert", help="Конвертировать величину")
    convert_parser.add_argument("value", type=float)
    convert_parser.add_argument("--from", dest="from_unit", required=True)
    convert_parser.add_argument("--to", dest="to_unit", required=True)

    argv = sys.argv[1:]
    if (len(argv) >= 2
        and argv[0] == "calc"
        and argv[1].startswith("-")
        and argv[1] not in ("-h", "--help", "--")
    ):
        argv.insert(1, "--")
    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            calc_result = calculate(args.expression)
            print(calc_result)

        elif args.command == "convert":
            convert_result = convert(args.value, args.from_unit, args.to_unit)
            print(convert_result)
    except ToolkitError as error:
        print(error, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
