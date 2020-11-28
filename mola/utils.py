import logging
import re
from re import Pattern
from typing import List

from colour import Color

# Pattern for matching HEX colors
HEX_PATTERN: Pattern = re.compile(r"(#[A-Fa-f0-9]{6}|#[A-Fa-f0-9]{3})")

# channel indexes
RED = 0
GREEN = 1
BLUE = 2
MODE_RGB = 'RGB'

LOG = logging.getLogger(__name__)


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


def luminance(color: Color) -> int:
    """
    Get the color's luminance in as an 8 bit int
    :param color: RGB color
    :return: luminance value
    """
    return int(round(255 * color.get_luminance()))


def to_array(color: Color) -> List[int]:
    """
    Represent a color object as an array of integers with values for separate RGB channels
    :param color: color object
    :return: list of RGB channel values in the color
    """
    return [int(round(color.get_red() * 255)), int(round(color.get_green() * 255)), int(round(color.get_blue() * 255))]


def print_theme(theme: List[Color], title: str, block_size: int = 3, line_size: int = 32, prefix: str = ''):
    """
    Print theme of colors in 32 character blocks
    :param theme: color theme
    :param title: title for the printed theme
    :param block_size: length of line block of a single color
    :param line_size: length of line of colors
    :param prefix: prefix of every line of colors
    """
    theme = sorted(theme, key=luminance)
    if LOG.isEnabledFor(logging.DEBUG):
        try:
            # noinspection PyPackageRequirements
            from sty import fg
            LOG.debug(title)
            block = '█' * block_size
            for i in range(len(theme)):
                if i % 32 == 0:
                    print(prefix, end='')
                print(f'{fg(*to_array(theme[i]))}{block}{fg.rs}', end='\n' if (i + 1) % line_size == 0 else '')
            if len(theme) < line_size:
                print(prefix, end='\n')
        except ImportError:
            # sty not available
            pass


def as_colors(colors: List[str]) -> List[Color]:
    """
    Convert list of HEX color representations into a list of color objects
    :param colors: list of HEX colors for a theme
    :return: list of colour.Color object
    """
    return [Color(color_hex) for color_hex in set(colors)]


def distance(color1, color2) -> float:
    """
    Measure distance between two colors using CIELAB color space
    :param color1: first color
    :param color2: second color
    :return: Euclidean distance between two colors in CIELAB color space
    """
    lab1 = rgb2lab(to_array(color1))
    lab2 = rgb2lab(to_array(color2))
    return pow(lab1[0] - lab2[0], 2) + pow(lab1[1] - lab2[1], 2) + pow(lab1[2] - lab2[2], 2)


def rgb2lab(input_color):
    """
    Convert between RGB and CIELAB color spaces following implementation from: https://stackoverflow.com/a/16020102
    :param input_color: color in RGB space
    :return: color in CIELAB space
    """
    num = 0
    rgb = [0, 0, 0]

    for value in input_color:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        rgb[num] = value * 100
        num = num + 1

    xyz = [0, 0, 0, ]

    x = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
    y = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
    z = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505
    xyz[0] = round(x, 4)
    xyz[1] = round(y, 4)
    xyz[2] = round(z, 4)

    xyz[0] = float(xyz[0]) / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
    xyz[1] = float(xyz[1]) / 100.0  # ref_Y = 100.000
    xyz[2] = float(xyz[2]) / 108.883  # ref_Z = 108.883

    num = 0
    for value in xyz:

        if value > 0.008856:
            value = value ** 1 / 3
        else:
            value = (7.787 * value) + (16 / 116)

        xyz[num] = value
        num = num + 1

    return [round((116 * xyz[1]) - 16, 4), round(500 * (xyz[0] - xyz[1]), 4), round(200 * (xyz[1] - xyz[2]), 4)]
