from typing import List

import matplotlib.pyplot as plt

import argparse
import sys

import numpy
from colour import Color
from skimage import io, exposure
from skimage.exposure import match_histograms

from mola.palettes import PALETTES


def gray(color: Color) -> int:
    return int(round(255 * (0.299 * color.get_red() + 0.587 * color.get_green() + 0.114 * color.get_blue())))


def gradient(c1: Color, c2: Color, count: int) -> List[Color]:
    return ([] + list(c1.range_to(c2, count)))[1:]


def colorize(params):
    if params.palette not in PALETTES:
        raise ValueError(f"Unknown palette {params.palette}")

    """
    Fetch palette and sort by darkness
    """
    palette = PALETTES[params.palette]
    palette.sort(key=lambda c: gray(c))

    """
    Read input image and prepare histogram
    """
    image = io.imread(params.image, as_gray=True)
    histogram, bin_centers = exposure.histogram(image)

    """
    Prepare colors according to the histogram
    """
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

    """
    Prepare reference palette image
    """
    reference = [[]]
    for i in range(len(colors)):
        count = histogram[i]
        if count > 0:
            reference[0].extend(
                count * [[int(round(colors[i].get_red() * 255)), int(round(colors[i].get_green() * 255)),
                          int(round(colors[i].get_blue() * 255))]])

    """
    Match histograms
    """
    image = io.imread(params.image)
    reference = numpy.array(reference)
    matched = match_histograms(image, reference, multichannel=True)

    """
    Save output file
    """
    io.imsave(params.output_file, matched)

    """
    Draw plot (TEMPORARY)
    """
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(8, 3))
    for aa in (ax1, ax2):
        aa.set_axis_off()

    ax1.imshow(image)
    ax1.set_title('Source')

    ax2.imshow(matched)
    ax2.set_title('Matched')

    plt.tight_layout()
    plt.show()


def run():
    parser = argparse.ArgumentParser(description="Colorize images with a specific palette")
    parser.add_argument("-p",
                        "--palette",
                        dest="palette",
                        help="name of the palette to use",
                        action="store",
                        type=str)
    parser.add_argument("image",
                        help="image to colorize")
    parser.add_argument("output_file",
                        help="output file name")

    colorize(parser.parse_args(sys.argv[1:]))


if __name__ == "__main__":
    run()
