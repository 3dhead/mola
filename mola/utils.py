# Pattern for matching HEX colors
import re
from re import Pattern
from typing import List

from colour import Color

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


def cred(color: Color) -> int:
    return int(round(color.get_red() * 255))


def cgreen(color: Color) -> int:
    return int(round(color.get_green() * 255))


def cblue(color: Color) -> int:
    return int(round(color.get_blue() * 255))


def to_array(color: Color) -> List[int]:
    return [cred(color), cgreen(color), cblue(color)]


def closest(color: Color, index: int) -> int:
    red_diff = abs(cred(color) - index)
    blue_diff = abs(cblue(color) - index)
    green_diff = abs(cgreen(color) - index)

    # select the number of pixels from the histogram of the channel which value is the
    # closest to the current color
    if red_diff < blue_diff and red_diff < green_diff:
        # red
        return 0
    elif green_diff < blue_diff and green_diff < red_diff:
        # green
        return 1
    else:
        # blue
        return 2
