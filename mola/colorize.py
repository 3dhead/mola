import logging
from math import ceil
from typing import List

import numpy
from colour import Color
from skimage.exposure import match_histograms

from mola.utils import gray, gradient, closest, RED, GREEN, BLUE

LOG = logging.getLogger(__name__)


def extend_theme(histograms, theme: List[Color]) -> List[Color]:
    """
    Match color theme to the histogram to produce 256 colors used to create the reference image
    :param histograms: image histograms
    :param theme: selected colors
    :return: 256 color theme
    """
    theme.sort(key=lambda c: gray(c))
    white_representation: Color = theme.pop()
    colors: List[Color] = [theme.pop(0)]
    i_last: int = 0
    for i in range(256):
        color = theme[0]
        if gray(color) == i:
            theme.pop(0)
            colors.extend(gradient(colors[len(colors) - 1], color, i - i_last))
            i_last = i
            if len(theme) == 0:
                break
    colors.extend(gradient(colors[len(colors) - 1], white_representation, 256 - len(colors) + 1))
    theme.extend(colors)
    return theme


def to_histogram(image):
    """
    Obtain histograms of an image
    :param image: RGB image
    :return: RGB histograms
    """
    red, _ = numpy.histogram(image[:, :, RED].ravel(), bins=256)
    green, _ = numpy.histogram(image[:, :, GREEN].ravel(), bins=256)
    blue, _ = numpy.histogram(image[:, :, BLUE].ravel(), bins=256)
    return [red, green, blue]


def create_reference_image(colors: List[Color], histograms, precision: float):
    """
    Produce a reference image used for histogram match against the original input image. The 256 color theme
    is used to create pixels roughly reflecting the histogram of the input image.
    :param colors: 256 color theme
    :param histograms: histograms of the input image
    :param precision: controls quality vs speed by reducing the number of pixels in the reference image
    :return: reference image for histogram match
    """
    reference = [[]]
    for i in range(len(colors)):
        # put the calculated number of pixels in the current color in the reference image
        closest_histogram, color_as_array = closest(colors[i], i)
        reference[0].extend(int(ceil(histograms[closest_histogram][i] * precision)) * [color_as_array])
    return reference


def colorize(image: numpy.ndarray, theme: List[Color], precision: float) -> numpy.ndarray:
    """
    Colorize input image with a selected list of colors.
    :param image: input image
    :param theme: selected list of colors
    :param precision: selected precision of the algorithm
    :return: colorized image
    """
    histograms = to_histogram(image)
    reference: List = create_reference_image(extend_theme(histograms, theme), histograms, precision)
    return match_histograms(image, numpy.array(reference), multichannel=True)
