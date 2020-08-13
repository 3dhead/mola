import argparse
import sys

from mola.colorize import colorize
from mola.feh import feh
from mola.palettes import list_palettes


def run():
    """
    Set up argument parser and run
    """

    parser = argparse.ArgumentParser(description="Colorize images with a specific palette")

    subparsers = parser.add_subparsers(help='')

    """
    mola colorize -p nord input.jpg output.jpg
    """
    parser_colorize = subparsers.add_parser('colorize', help='colorize an image')
    parser_colorize.add_argument("palette",
                                 help="name of the palette to use")
    parser_colorize.add_argument("image",
                                 help="image to colorize")
    parser_colorize.add_argument("output_file",
                                 help="output file name")
    parser_colorize.set_defaults(func=colorize)

    """
    mola palettes
    """
    parser_list_palettes = subparsers.add_parser('palettes', help='print list of available palettes')
    parser_list_palettes.set_defaults(func=list_palettes)

    """
    mola feh -p nord input.jpg (any additional feh arguments)
    """
    parser_feh = subparsers.add_parser('feh', help='colorize an image and set as background')
    parser_feh.add_argument("palette",
                            help="name of the palette to use")
    parser_feh.add_argument("image",
                            help="image to colorize")
    parser_feh.set_defaults(func=feh)

    args, additional_params = parser.parse_known_args(sys.argv[1:])
    args.func(args, additional_params)


if __name__ == "__main__":
    run()
