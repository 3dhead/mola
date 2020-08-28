import logging
import re
import sys
from math import ceil
from re import Pattern
from typing import List

import numpy
from colour import Color
from skimage import io, exposure
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from sty import fg

from mola.themes import THEMES, of

LOG = logging.getLogger(__name__)

# Pattern for matching HEX colors
HEX_PATTERN: Pattern = re.compile(r"(#[A-Fa-f0-9]{6}|#[A-Fa-f0-9]{3})")


def get_theme(params):
    theme = None
    if params.theme not in THEMES:
        LOG.debug(f"Unmatched theme '{params.theme}'. Trying to find HEX color codes in the argument.")

        # Try to discover colors directly from the string
        match = HEX_PATTERN.findall(params.theme)
        if match and len(match) > 0:
            LOG.debug(f"Regexp matching produced {len(match)} colors")
            theme = of(match)

        if not theme:
            LOG.error(f"Unknown theme {params.theme}")
            sys.exit(1)
    else:
        theme = THEMES[params.theme]

    # Verify theme
    if len(theme) < 3:
        LOG.error(f"A theme needs more than 2 colors ({len(theme)} given)")
        sys.exit(1)
    return theme


def gray(color: Color) -> int:
    """
    Calculate the gray scale of an RGB color
    :param color: RGB color
    :return: gray scale value
    """
    return int(round(255 * (0.299 * color.get_red() + 0.587 * color.get_green() + 0.114 * color.get_blue())))


def gradient(c1: Color, c2: Color, count: int) -> List[Color]:
    """
    Calculate a gradient of a given length between two colors
    :param c1: first color
    :param c2: second color
    :param count: number of colors in the gradient
    :return: list of colors in the gradient excluding the first color: (c1; c2>
    """
    return ([] + list(c1.range_to(c2, count)))[1:]


def match_colors(histogram, theme: List[Color]) -> List[Color]:
    """

    :param histogram:
    :param theme:
    :return:
    """
    theme.sort(key=lambda c: gray(c))
    white_representation: Color = theme.pop()
    colors: List[Color] = [theme.pop(0)]
    i_last: int = 0
    for i in range(len(histogram)):
        color = theme[0]
        if gray(color) == i:
            theme.pop(0)
            colors.extend(gradient(colors[len(colors) - 1], color, i - i_last))
            i_last = i
            if len(theme) == 0:
                break
    colors.extend(gradient(colors[len(colors) - 1], white_representation, len(histogram) - len(colors) + 1))
    return colors


def to_histogram(image):
    """

    :param image:
    :return:
    """
    histogram, bin_centers = exposure.histogram(rgb2gray(image))
    # red, _ = exposure.histogram(image[:, :, 0])
    # green, _ = exposure.histogram(image[:, :, 1])
    # blue, _ = exposure.histogram(image[:, :, 2])
    # histograms = [red, green, blue]
    return histogram


def create_reference_image(colors: List[Color], histogram, precision: float):
    """

    :param colors:
    :param histogram:
    :param precision:
    :return:
    """
    reference = [[]]
    for i in range(len(colors)):
        count = int(ceil(histogram[i] * precision))
        red = int(round(colors[i].get_red() * 255))
        green = int(round(colors[i].get_green() * 255))
        blue = int(round(colors[i].get_blue() * 255))
        # TODO how to log this
        if i % 32 == 0:
            print('\t', end='')
        print(f'{fg(red, green, blue)}█{fg.rs}', end='\n' if (i + 1) % 32 == 0 else '')
        reference[0].extend(count * [[red, green, blue]])
    return reference


def colorize_image(image, theme: List[Color], precision: float):
    """

    :param image:
    :param theme:
    :param precision:
    :return:
    """
    histogram = to_histogram(image)
    reference = create_reference_image(match_colors(histogram, theme), histogram, precision)
    return match_histograms(image, numpy.array(reference), multichannel=True)


def colorize(params, *_unused):
    # verify selected precision
    if params.precision <= 0 or params.precision > 1:
        LOG.error(f"--precision must be in range: (0, 1> ({params.precision} given)")
        sys.exit(1)

    # determine target theme
    theme = get_theme(params)

    try:
        # read source image
        image = io.imread(params.image)
    except IOError as err:
        LOG.info(f"Failed to read file {params.image}. Use --debug for more information")
        LOG.debug(err)
        sys.exit(1)

    # colorize image
    matched = colorize_image(image, theme, params.precision)

    try:
        # save output
        io.imsave(params.output_file, matched, quality=100)
    except IOError as err:
        LOG.info(f"Failed to save file to {params.output_file}. Use --debug for more information")
        LOG.debug(err)
        sys.exit(1)
