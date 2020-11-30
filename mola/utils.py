import colorsys
import logging
import re
from math import sqrt
from re import Pattern
from typing import List

from PIL import ImageColor

HEX_PATTERN: Pattern = re.compile(r"(#[A-Fa-f0-9]{6}|#[A-Fa-f0-9]{3})")  # Pattern for matching HEX colors

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


def luminance(color) -> float:
    """
    Get the color's luminance in as an 8 bit int
    :param color: RGB color
    :return: luminance value
    """
    return colorsys.rgb_to_hls(*[x / 255.0 for x in color])[1]


def with_luminance(color, brightness):
    """
    Adjust RGB color luminance
    :param color: RGB color
    :param brightness: new luminance value
    :return: RGB with modified luminance
    """
    hls = colorsys.rgb_to_hls(*[x / 255.0 for x in color])
    return [int(round(x * 255.0)) for x in colorsys.hls_to_rgb(hls[0], brightness, hls[2])]


def print_theme(theme: List, title: str, block_size: int = 3, line_size: int = 32, prefix: str = ''):
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
                print(f'{fg(*theme[i])}{block}{fg.rs}', end='\n' if (i + 1) % line_size == 0 else '')
            if len(theme) < line_size:
                print(prefix, end='\n')
        except ImportError:
            # sty not available
            pass


def as_colors(colors: List[str]) -> List:
    """
    Convert list of HEX color representations into a list of color objects
    :param colors: list of HEX colors for a theme
    :return: list of RGB colors
    """
    return [ImageColor.getcolor(color_hex, MODE_RGB) for color_hex in set(colors)]


def distance(color1, color2) -> float:
    """
    Measure distance between two colors using HSL color space
    :param color1: first color
    :param color2: second color
    :return: Euclidean distance between two colors in HSL color space
    """
    hls1 = colorsys.rgb_to_hls(*[x / 255.0 for x in color1])
    hls2 = colorsys.rgb_to_hls(*[x / 255.0 for x in color2])
    dl = min(abs(hls1[1] - hls2[1]), 1 - abs(hls1[1] - hls2[1])) / 2
    ds = hls1[2] - hls2[2]
    return sqrt(dl * dl + ds * ds)
