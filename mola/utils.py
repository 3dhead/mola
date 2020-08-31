import re
from re import Pattern
from typing import List

from colour import Color
from sty import fg

# Pattern for matching HEX colors
HEX_PATTERN: Pattern = re.compile(r"(#[A-Fa-f0-9]{6}|#[A-Fa-f0-9]{3})")

# channel indexes
RED = 0
GREEN = 1
BLUE = 2


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


def to_array(color: Color) -> List[int]:
    """
    Represent a color object as an array of integers with values for separate RGB channels
    :param color: color object
    :return: list of RGB channel values in the color
    """
    return [int(round(color.get_red() * 255)), int(round(color.get_green() * 255)), int(round(color.get_blue() * 255))]


def closest(color: Color, channel_value: int) -> (int, List[int]):
    """
    Select channel of the color with value closest to the given one
    :param color: color to test
    :param channel_value: value of the color in channel
    :return: index of the channel with the closest value and color represented as an array of integers
    """
    color_as_array = to_array(color)
    diffs = [abs(color_as_array[RED] - channel_value), abs(color_as_array[GREEN] - channel_value),
             abs(color_as_array[BLUE] - channel_value)]
    return diffs.index(min(diffs)), color_as_array


def print_theme(theme: List[Color], block_size: int = 1, line_size: int = 32, prefix: str = ''):
    """
    Print theme of colors in 32 character blocks
    :param theme: color theme
    :param block_size: length of line block of a single color
    :param line_size: length of line of colors
    :param prefix: prefix of every line of colors
    """
    block = '█' * block_size
    for i in range(len(theme)):
        if i % 32 == 0:
            print(prefix, end='')
        print(f'{fg(*to_array(theme[i]))}{block}{fg.rs}', end='\n' if (i + 1) % line_size == 0 else '')


def as_colors(colors: List[str]) -> List[Color]:
    """
    Convert list of HEX color representations into a list of color objects
    :param colors: list of HEX colors for a theme
    :return: list of colour.Color object
    """
    return [Color(color_hex) for color_hex in set(colors)]
