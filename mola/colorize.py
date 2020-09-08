import logging
from math import ceil
from typing import List

import numpy
from colour import Color
from skimage.exposure import match_histograms
from skimage.transform import resize

from mola.utils import luminance, gradient, RED, GREEN, BLUE, is_mostly, print_theme, to_array

LOG = logging.getLogger(__name__)


def channel_theme(theme: List[Color], channel: int, white: Color, black: Color) -> List[Color]:
    # noinspection PyTypeChecker
    c_theme: List[Color] = [None] * 256
    c_theme[0] = black
    c_theme[255] = white

    # select colors related to the channel
    for color in theme:
        if is_mostly(color, channel):
            c_theme[luminance(color)] = color

    # fill gaps with gradient
    last_filled = -1
    for index in range(len(c_theme)):
        if c_theme[index] is None or index <= last_filled:
            continue
        if last_filled >= 0:
            fill = gradient(c_theme[last_filled], c_theme[index], index - last_filled)
            for i in range(len(fill)):
                c_theme[last_filled + 1 + i] = fill[i]
        last_filled = index

    print_theme(c_theme)

    return c_theme


def create_theme(histograms, theme: List[Color]) -> List[Color]:
    """
    Match color theme to the histogram to produce 256 colors used to create the reference image
    :param histograms: image histograms
    :param theme: selected colors
    :return: 256 color theme
    """
    theme.sort(key=lambda color: luminance(color))
    white: Color = theme.pop()
    black: Color = theme.pop(0)
    channel_themes = []
    for channel in [RED, GREEN, BLUE]:
        channel_themes.append(channel_theme(theme, channel, white, black))

    theme.clear()
    for i in range(256):
        total = histograms[RED][i] + histograms[GREEN][i] + histograms[BLUE][i]
        if total == 0:
            # append black since this won't be in the reference image anyway - no values in histogram
            theme.append(Color())
            continue
        red_part = histograms[RED][i] / total
        green_part = histograms[GREEN][i] / total
        blue_part = histograms[BLUE][i] / total

        red = channel_themes[RED][i]
        green = channel_themes[GREEN][i]
        blue = channel_themes[BLUE][i]

        # linear interpolation in the HSL space
        c = Color()
        c.set_hue(red_part * red.get_hue() + green_part * green.get_hue() + blue_part * blue.get_hue())
        c.set_saturation(
            red_part * red.get_saturation() + green_part * green.get_saturation() + blue_part * blue.get_saturation())
        c.set_luminance(
            red_part * red.get_luminance() + green_part * green.get_luminance() + blue_part * blue.get_luminance())

        theme.append(c)
    return theme


def to_histogram(image, precision: int):
    """
    Obtain histograms of an image
    :param image: RGB image
    :param precision: pre-scale factor for histogram analysis
    :return: RGB histograms
    """
    if precision < 100:
        # pre-scale the original image for histogram analysis
        image = resize(image, (image.shape[0] * precision // 100, image.shape[1] * precision // 100))
    red, _ = numpy.histogram(image[:, :, RED].ravel(), bins=256)
    green, _ = numpy.histogram(image[:, :, GREEN].ravel(), bins=256)
    blue, _ = numpy.histogram(image[:, :, BLUE].ravel(), bins=256)
    return [red, green, blue]


def create_reference_image(colors: List[Color], histograms):
    """
    Produce a reference image used for histogram match against the original input image. The 256 color theme
    is used to create pixels roughly reflecting the histogram of the input image.
    :param colors: 256 color theme
    :param histograms: histograms of the input image
    :return: reference image for histogram match
    """
    reference = [[]]
    for i in range(len(colors)):
        # put the calculated number of pixels in the current color in the reference image
        values_in_channel = [histograms[RED][i], histograms[GREEN][i], histograms[BLUE][i]]
        selected_channel = values_in_channel.index(max(values_in_channel))
        reference[0].extend(int(ceil(histograms[selected_channel][i])) * [to_array(colors[i])])
    return reference


def colorize(image: numpy.ndarray, theme: List[Color], precision: int) -> numpy.ndarray:
    """
    Colorize input image with a selected list of colors.
    :param image: input image
    :param theme: selected list of colors
    :param precision: selected precision of the algorithm
    :return: colorized image
    """
    histograms = to_histogram(image, precision)
    reference: List = create_reference_image(create_theme(histograms, theme), histograms)
    return match_histograms(image, numpy.array(reference), multichannel=True)
