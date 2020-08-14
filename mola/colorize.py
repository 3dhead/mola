import logging
import sys
import time
from math import ceil
from typing import List

import numpy
from colour import Color
from skimage import io, exposure
from skimage.exposure import match_histograms

from mola.palettes import PALETTES

LOG = logging.getLogger(__name__)


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


def colorize(params, *_unused):
    """
    Verify selected palette
    """
    if params.palette not in PALETTES:
        LOG.error(f"Unknown palette {params.palette}")
        sys.exit(1)

    """
    Verify selected precision
    """
    if params.precision <= 0 or params.precision > 1:
        LOG.error(f"--precision must be in range: (0, 1> ({params.precision} given)")
        sys.exit(1)

    LOG.info("Running colorize...")
    start = time.time()

    """
    Fetch palette and sort by darkness
    """
    palette = PALETTES[params.palette]
    palette.sort(key=lambda c: gray(c))

    """
    Read input image and prepare histogram
    """
    now = time.time()
    LOG.debug("Preparing histograms...")
    image = io.imread(params.image, as_gray=True)
    histogram, bin_centers = exposure.histogram(image)
    LOG.debug("Done in {:.2f}s".format(time.time() - now))
    # red, _ = exposure.histogram(image[:, :, 0])
    # green, _ = exposure.histogram(image[:, :, 1])
    # blue, _ = exposure.histogram(image[:, :, 2])
    # histograms = [red, green, blue]

    """
    Prepare colors according to the histogram
    """
    now = time.time()
    LOG.debug("Preparing palette...")
    white_representation: Color = palette.pop()
    colors: List[Color] = [palette.pop(0)]
    i_last: int = 0
    for i in range(len(histogram)):
        color = palette[0]
        if gray(color) == i:
            palette.pop(0)
            colors.extend(gradient(colors[len(colors) - 1], color, i - i_last))
            i_last = i
            if len(palette) == 0:
                break
    colors.extend(gradient(colors[len(colors) - 1], white_representation, len(histogram) - len(colors) + 1))
    LOG.debug("Done in {:.2f}s".format(time.time() - now))

    """
    Prepare reference palette image
    """
    now = time.time()
    LOG.debug(f"Preparing reference image with precision {params.precision}...")
    reference = [[]]
    for i in range(len(colors)):
        count = int(ceil(histogram[i] * params.precision))
        reference[0].extend(
            count * [[int(round(colors[i].get_red() * 255)), int(round(colors[i].get_green() * 255)),
                      int(round(colors[i].get_blue() * 255))]])
    LOG.debug("Done in {:.2f}s".format(time.time() - now))

    """
    Match histograms
    """
    now = time.time()
    LOG.debug("Running histogram match...")
    image = io.imread(params.image)
    reference = numpy.array(reference)
    matched = match_histograms(image, reference, multichannel=True)
    LOG.debug("Done in {:.2f}s".format(time.time() - now))

    """
    Save output file
    """
    now = time.time()
    LOG.debug(f"Saving output to {params.output_file}...")
    io.imsave(params.output_file, matched)
    LOG.debug("Done in {:.2f}s".format(time.time() - now))

    LOG.info("Total time: {:.2f}s".format(time.time() - start))
