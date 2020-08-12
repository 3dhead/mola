import subprocess
import tempfile
from typing import List

import argparse
import sys

import numpy
from colour import Color
from skimage import io, exposure
from skimage.exposure import match_histograms

from mola.palettes import PALETTES


def gray(color: Color) -> int:
    return int(round(255 * (0.299 * color.get_red() + 0.587 * color.get_green() + 0.114 * color.get_blue())))


def gradient(c1: Color, c2: Color, count: int) -> List[Color]:
    return ([] + list(c1.range_to(c2, count)))[1:]


# noinspection PyUnusedLocal
def list_palettes(params, *_unused):
    """
    Prints list of all palettes available in the configuration
    :param params: unused
    """
    for palette_name in PALETTES.keys():
        print(palette_name)


def colorize(params, *_unused):
    if params.palette not in PALETTES:
        raise ValueError(f"Unknown palette {params.palette}")

    """
    Fetch palette and sort by darkness
    """
    palette = PALETTES[params.palette]
    palette.sort(key=lambda c: gray(c))

    """
    Read input image and prepare histogram
    """
    image = io.imread(params.image, as_gray=True)
    histogram, bin_centers = exposure.histogram(image)

    """
    Prepare colors according to the histogram
    """
    white_representation: Color = palette.pop()
    colors: List[Color] = [palette.pop(0)]
    i_last: int = 0
    for i in range(len(histogram)):
        color = palette[0]
        if gray(color) == i:
            palette.pop(0)
            colors.extend(gradient(colors[len(colors) - 1], color, i - i_last))
            i_last = i
            if len(palette) == 0:
                break
    colors.extend(gradient(colors[len(colors) - 1], white_representation, len(histogram) - len(colors) + 1))

    """
    Prepare reference palette image
    """
    reference = [[]]
    for i in range(len(colors)):
        count = histogram[i]
        if count > 0:
            reference[0].extend(
                count * [[int(round(colors[i].get_red() * 255)), int(round(colors[i].get_green() * 255)),
                          int(round(colors[i].get_blue() * 255))]])

    """
    Match histograms
    """
    image = io.imread(params.image)
    reference = numpy.array(reference)
    matched = match_histograms(image, reference, multichannel=True)

    """
    Save output file
    """
    io.imsave(params.output_file, matched)


def feh(params, additional_params: List):
    temporary_image = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    params.output_file = temporary_image.name
    temporary_image.close()
    colorize(params)
    subprocess.run(["feh"] + additional_params + [params.output_file])


def run():
    parser = argparse.ArgumentParser(description="Colorize images with a specific palette")

    subparsers = parser.add_subparsers(help='')

    """
    mola colorize -p nord input.jpg output.jpg
    """
    parser_colorize = subparsers.add_parser('colorize', help='colorize an image')
    parser_colorize.add_argument("-p",
                                 "--palette",
                                 dest="palette",
                                 help="name of the palette to use",
                                 action="store",
                                 type=str)
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
    parser_feh.add_argument("-p",
                            "--palette",
                            dest="palette",
                            help="name of the palette to use",
                            action="store",
                            type=str)
    parser_feh.add_argument("image",
                            help="image to colorize")
    parser_feh.set_defaults(func=feh)

    args, additional_params = parser.parse_known_args(sys.argv[1:])
    args.func(args, additional_params)


if __name__ == "__main__":
    run()
