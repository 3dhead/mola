import logging
import re
from math import ceil
from re import Pattern
from typing import List

import numpy
from colour import Color
from skimage import exposure
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from sty import fg

LOG = logging.getLogger(__name__)

# Pattern for matching HEX colors
HEX_PATTERN: Pattern = re.compile(r"(#[A-Fa-f0-9]{6}|#[A-Fa-f0-9]{3})")


def hex_color(value: str) -> str:
    """
    Validate a string is a HEX color representation
    :param value: potentially a HEX color
    :return: the same value, error raised the value is not correct
    """
    if HEX_PATTERN.fullmatch(value):
        return value
    else:
        raise ValueError


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
    Match color theme to the histogram to produce 256 colors used to create the reference image
    :param histogram: image histogram
    :param theme: selected colors
    :return: 256 color theme
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
    Obtain histogram of an image
    :param image: RGB image
    :return:gray scale histogram
    """
    histogram, bin_centers = exposure.histogram(rgb2gray(image))
    # red, _ = exposure.histogram(image[:, :, 0])
    # green, _ = exposure.histogram(image[:, :, 1])
    # blue, _ = exposure.histogram(image[:, :, 2])
    # histograms = [red, green, blue]
    return histogram


def create_reference_image(colors: List[Color], histogram, precision: float):
    """
    Produce a reference image used for histogram match against the original input image. The 256 color theme
    is used to create pixels roughly reflecting the histogram of the input image.
    :param colors: 256 color theme
    :param histogram: histogram of the input image
    :param precision: controls quality vs speed by reducing the number of pixels in the reference image
    :return: reference image for histogram match
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


def colorize(image, theme: List[Color], precision: float):
    """
    Colorize input image with a selected list of colors.
    :param image: input image
    :param theme: selected list of colors
    :param precision: selected precision of the algorithm
    :return: colorized image
    """
    histogram = to_histogram(image)
    reference = create_reference_image(match_colors(histogram, theme), histogram, precision)
    return match_histograms(image, numpy.array(reference), multichannel=True)
