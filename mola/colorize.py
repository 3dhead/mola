import itertools
import logging
from typing import List

import numpy
from PIL import Image
from skimage.exposure import match_histograms

from mola.utils import print_theme, distance, MODE_RGB, with_luminance, luminance

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

    theme = [min(theme, key=lambda c: distance(c if aggressive else with_luminance(c, luminance(source)), source)) for
             source in image_palette]
    print_theme(theme, "Target image theme:")

    target_palette = list(itertools.chain(*theme))

    p_img = Image.new('P', (1, 1))
    p_img.putpalette(target_palette * int(768 / len(target_palette)))

    p = image.quantize(palette=p_img, dither=0).convert(MODE_RGB)
    if precision < 100:
        size = (int(round(p.size[0] * precision / 100)), int(round(p.size[1] * precision / 100)))
        LOG.debug(f"Resizing reference image to {size}")
        p = p.resize(size)

    reference = numpy.array(p.getdata()).reshape((p.size[0], p.size[1], 3))
    return match_histograms(numpy.asarray(image), reference, multichannel=True)
