import argparse


def check_level(value):
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid level value")
    if 0 <= value <= 254:
        return value
    else:
        raise argparse.ArgumentTypeError("Invalid level value")


def getArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--debug", action='store_true')

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = False

    parser_config = subparsers.add_parser("config")
    parser_config.add_argument("IP")
    parser_config.add_argument("KEY")

    subparsers.add_parser("on").add_argument("ID")
    subparsers.add_parser("off").add_argument("ID")

    subparsers.add_parser("server")
    subparsers.add_parser("http")

    subparsers.add_parser("list")
    subparsers.add_parser("test")

    # subparsers.add_parser("pair")

    parser_level = subparsers.add_parser("level")
    parser_level.add_argument("ID")
    parser_level.add_argument("value", type=check_level)
    parser_level.add_argument(
        "--transition_time",
        nargs='?',
        default=10,
        type=int)

    parser_colortemp = subparsers.add_parser("whitetemp")
    parser_colortemp.add_argument("ID")
    parser_colortemp.add_argument("value", choices=['cold', 'normal', 'warm'])

    parser_hex = subparsers.add_parser("hex")
    parser_hex.add_argument("ID")
    parser_hex.add_argument("value")

    parser_hsb = subparsers.add_parser("hsb")
    parser_hsb.add_argument("ID")
    parser_hsb.add_argument("hue")
    parser_hsb.add_argument("saturation")
    parser_hex.add_argument("brightness", nargs="?")

    parser_rgb = subparsers.add_parser("rgb")
    parser_rgb.add_argument("ID")
    parser_rgb.add_argument("red", type=int)
    parser_rgb.add_argument("green", type=int)
    parser_rgb.add_argument("blue", type=int)

    subparsers.add_parser("raw").add_argument("ID")

    subparsers.add_parser("observe")

    return parser.parse_args()
