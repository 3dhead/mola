import itertools
import logging
import math
from typing import List

import numpy
from PIL import Image
from skimage.exposure import match_histograms

from mola.utils import print_theme, distance, MODE_RGB, assume_luminance, luminance

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

    extracted = 0 if len(color_counts) == 0 else 2 ** math.floor(math.log2(len(color_counts)))
    LOG.debug(f"Extracted {extracted} colors from the image.")
    for i in range(extracted):
        palette_index = color_counts[i][1]
        yield palette[palette_index * 3:palette_index * 3 + 3]


def colorize(image: Image, theme: List, aggressive: bool, precision: int):
    """
    Colorize input image with a selected list of colors.
    :param image: input image
    :param theme: selected list of colors
    :param aggressive: true if colorizing should be more aggressive
    :param precision: selected precision of the algorithm
    :return: colorized image
    """
    print_theme(theme, "User theme:")

    theme = sorted(theme, key=luminance)
    image_palette = extract_palette(image)

    result = []
    for source in image_palette:
        closest = min(theme, key=lambda c: distance(c, source))
        if not aggressive:
            closest = assume_luminance(closest, source)
        result.append(closest)
    palette = list(itertools.chain(*result))

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
