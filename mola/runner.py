import argparse
import logging
import sys
import time

from mola.colorize import colorize
from mola.feh import feh
from mola.themes import list_themes


def run():
    """
    Set up argument parser and run
    """

    parser = argparse.ArgumentParser(description="Colorize images with a specific theme")

    parser.add_argument(
        "-v",
        dest="log_level",
        help="enable verbose logging",
        action="store_const",
        const=logging.DEBUG,
        default=logging.INFO
    )

    subparsers = parser.add_subparsers(help='')

    """
    mola colorize -p nord input.jpg output.jpg
    """
    parser_colorize = subparsers.add_parser('colorize', help='colorize an image')
    parser_colorize.add_argument("--precision",
                                 dest="precision",
                                 help="Processing precision in range (0; 1>, 1 being the slowest",
                                 action="store",
                                 type=float,
                                 default=0.9
                                 )
    parser_colorize.add_argument("theme",
                                 help="name of the theme to use or a list of HEX colors to use")
    parser_colorize.add_argument("image",
                                 help="image to colorize")
    parser_colorize.add_argument("output_file",
                                 help="output file name")
    parser_colorize.set_defaults(func=colorize)

    """
    mola themes
    """
    parser_list_themes = subparsers.add_parser('themes', help='print list of available themes')
    parser_list_themes.set_defaults(func=list_themes)

    """
    mola feh -p nord input.jpg (any additional feh arguments)
    """
    parser_feh = subparsers.add_parser('feh', help='colorize an image and set as background')
    parser_feh.add_argument("--precision",
                            dest="precision",
                            help="Processing precision in range (0; 1>, 1 being the slowest",
                            action="store",
                            type=float,
                            default=0.9
                            )
    parser_feh.add_argument("theme",
                            help="name of the theme to use or a list of HEX colors to use")
    parser_feh.add_argument("image",
                            help="image to colorize")
    parser_feh.set_defaults(func=feh)

    args, additional_params = parser.parse_known_args(sys.argv[1:])
    logging.basicConfig(level=args.log_level, stream=sys.stdout, format="%(levelname)s\t%(name)s: %(message)s")

    log = logging.getLogger(__name__)
    if len(additional_params) > 0:
        log.debug(f"Unknown arguments: {additional_params}")
    start = time.time()
    args.func(args, additional_params)
    log.info("Done. That took {:.2f}s".format(time.time() - start))


if __name__ == "__main__":
    run()
