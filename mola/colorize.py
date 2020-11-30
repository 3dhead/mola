import logging
from copy import deepcopy
from typing import List

import numpy
from PIL import Image
from colour import Color
from skimage.exposure import match_histograms

from mola.utils import to_array, print_theme, distance, MODE_RGB

LOG = logging.getLogger(__name__)


def extract_palette(img):
    """
    Extract 256 color palette from an input image
    :param img: pillow image
    :return: 256 color palette of most dominant colors in the image
    """
    copy = img.copy()
    paletted = copy.convert('P', palette=Image.ADAPTIVE)
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)

    size = 256
    while len(color_counts) < size:
        LOG.debug(f"Failed to extract {size} colors from the image. Trying with a smaller palette.")
        size = int(size / 2)
    for i in range(size):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index * 3:palette_index * 3 + 3]
        color = Color()
        color.set_red(dominant_color[0] / 255.0)
        color.set_green(dominant_color[1] / 255.0)
        color.set_blue(dominant_color[2] / 255.0)
        yield color


def colorize(image: Image, theme: List[Color], aggressive: bool, precision: int):
    """
    Colorize input image with a selected list of colors.
    :param image: input image
    :param theme: selected list of colors
    :param aggressive: true if colorizing should be more aggressive
    :param precision: selected precision of the algorithm
    :return: colorized image
    """

    print_theme(theme, "User theme:")

    palette = []
    result = []
    image_palette = extract_palette(image)
    for original in image_palette:
        min_diff = -1
        closest = Color("white")
        for from_palette in theme:
            color = from_palette
            if not aggressive:
                color = deepcopy(from_palette)
                color.set_luminance(original.get_luminance())
            diff = distance(color, original)
            if min_diff < 0 or diff < min_diff:
                min_diff = diff
                closest = color
        result.append(closest)
        palette += to_array(closest)

    print_theme(result, "Target image theme:")

    p_img = Image.new('P', (1, 1))
    p_img.putpalette(palette * int(768 / len(palette)))

    p = image.quantize(palette=p_img, dither=0).convert(MODE_RGB)
    if precision < 100:
        size = (int(round(p.size[0] * precision / 100)), int(round(p.size[1] * precision / 100)))
        LOG.debug(f"Resizing reference image to {size}")
        p = p.resize(size)

    reference = numpy.array(p.getdata()).reshape((p.size[0], p.size[1], 3))
    return match_histograms(numpy.asarray(image), reference, multichannel=True)
