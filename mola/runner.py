import argparse
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time

from PIL import Image
from skimage import io

from mola.colorize import colorize
from mola.themes import THEMES
from mola.utils import hex_color, HEX_PATTERN, as_colors


def parser() -> argparse.ArgumentParser:
    args = argparse.ArgumentParser(description="Colorize images with a selected color theme")

    # verbose logging
    args.add_argument("-v", "--verbose", dest="log_level", help="enable verbose logging", action="store_const",
                      const=logging.DEBUG, default=logging.ERROR)

    source = args.add_mutually_exclusive_group()

    # theme
    source.add_argument("-t", "--theme", dest="theme", help="name of the theme to use", choices=THEMES.keys(),
                        required=False)

    # file to parse
    source.add_argument("-f", "--file", dest="theme_file", help="file to parse for colors", required=False)

    # list of colors
    args.add_argument('-c', "--color", dest="color", help="list of HEX colors to use", type=hex_color, action='append',
                      required=False)

    # precision
    args.add_argument("-p", "--precision", dest="precision", type=int, default=100,
                      help="Processing precision in range 1-100, 100 being the slowest but most accurate")

    # input image
    args.add_argument("input", help="image to colorize")

    # output image - if not provided mola will run feh --bg-scale with the output instead
    output = args.add_mutually_exclusive_group()
    output.add_argument("-o", "--output", dest="output", help="output file", required=False)

    # feh options
    output.add_argument("--bg-center", dest="feh_opt", action="store_const", const="--bg-center", required=False)
    output.add_argument("--bg-fill", dest="feh_opt", action="store_const", const="--bg-fill", required=False)
    output.add_argument("--bg-max", dest="feh_opt", action="store_const", const="--bg-max", required=False)
    output.add_argument("--bg-scale", dest="feh_opt", action="store_const", const="--bg-scale", required=False)
    output.add_argument("--bg-tile", dest="feh_opt", action="store_const", const="--bg-tile", required=False)

    return args


def run():
    """
    Set up argument parser and run
    """

    args = parser().parse_args(sys.argv[1:])
    logging.basicConfig(level=args.log_level, stream=sys.stdout, format="%(levelname)s\t%(name)s: %(message)s")

    log = logging.getLogger(__name__)

    start = time.time()

    if args.precision < 1 or args.precision > 100:
        log.error(f"Precision value must be in range 1-100 ({args.precision} given)")
        sys.exit(1)

    # determine target theme
    theme = []
    if args.theme:
        if args.theme not in THEMES.keys():
            log.error(f"Unmatched theme '{args.theme}'")
            sys.exit(1)
        log.debug(f"Using theme '{args.theme}'")
        theme += THEMES[args.theme]
    if args.theme_file:
        try:
            with open(args.theme_file, 'r') as theme_file:
                log.debug(f"Parsing file '{args.theme_file}' for colors")
                colors = []
                for line in theme_file.readlines():
                    match = HEX_PATTERN.findall(line)
                    colors += match if match and len(match) > 0 else []
                log.debug(f"Extracted {len(colors)} colors from the theme file")
                theme += colors
        except IOError as err:
            log.error(f"Failed to read file '{args.theme_file}'")
            log.debug(err)
            sys.exit(1)
    if args.color:
        log.debug(f"Parsed {len(args.color)} colors from cli: {args.color}")
        theme += args.color

    # Verify theme
    if 256 < len(theme) < 3:
        log.error(f"A theme needs more than 2 colors but less than 257 ({len(theme)} given)")
        sys.exit(1)

    call_feh = False
    if not args.output:
        # check if feh is installed
        if not shutil.which("feh"):
            log.error("'feh' doesn't seem to be available in the system")
            sys.exit(1)
        call_feh = True

    try:
        # read source image
        log.debug(f"Using input file '{args.input}'")
        image: Image = Image.open(args.input)
        if image.mode != "RGB":
            # validate the input image is RGB
            log.error(f"Input image doesn't appear to be a color image")
            sys.exit(1)
    except IOError as err:
        log.error(f"Failed to read file {args.input}. Use --debug for more information")
        log.debug(err)
        sys.exit(1)

    # run colorizing
    log.debug(f"Running colorize with precision {args.precision}")
    theme = as_colors(theme)
    image = colorize(image, theme, args.precision)

    try:
        # save output
        if call_feh:
            _, file_extension = os.path.splitext(args.input)
            with tempfile.NamedTemporaryFile(suffix=file_extension) as temp:
                args.output = temp.name
        log.debug(f"Using output path '{args.output}'")
        io.imsave(args.output, image)
    except IOError as err:
        log.error(f"Failed to save file to {args.output}. Use -v for more information")
        log.debug(err)
        sys.exit(1)

    if call_feh:
        # call feh to set wallpaper
        feh_attributes = [temp.name, '--no-fehbg', args.feh_opt if args.feh_opt else '--bg-scale']
        log.debug(f"Running feh with attributes: {feh_attributes}")
        subprocess.run(["feh"] + feh_attributes)

    log.debug("Done. That took {:.2f}s".format(time.time() - start))


if __name__ == "__main__":
    run()
