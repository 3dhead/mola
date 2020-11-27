from copy import deepcopy
from typing import List

from PIL import Image
from colour import Color

from mola.utils import to_array, print_theme, luminance, rgb2lab


def get_image_palette(img) -> List[Color]:
    copy = img.copy()
    paletted = copy.convert('P', palette=Image.ADAPTIVE)
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = []
    for i in range(256):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index * 3:palette_index * 3 + 3]
        color = Color()
        color.set_red(dominant_color[0] / 255.0)
        color.set_green(dominant_color[1] / 255.0)
        color.set_blue(dominant_color[2] / 255.0)
        colors.append(color)
    return colors


def distance(color1, color2):
    lab1 = rgb2lab(to_array(color1))
    lab2 = rgb2lab(to_array(color2))
    return pow(lab1[0] - lab2[0], 2) + pow(lab1[1] - lab2[1], 2) + pow(lab1[2] - lab2[2], 2)


def colorize(image: Image, theme: List[Color]):
    print_theme(theme, "theme", block_size=3)

    palette = []
    result = []
    for original in get_image_palette(image):
        min_diff = 3 * 255 * 255 + 1
        closest = Color("#ffffff")
        for from_palette in theme:
            cloned = deepcopy(from_palette)
            cloned.set_luminance(original.get_luminance())
            diff = distance(cloned, original)
            if diff < min_diff:
                min_diff = diff
                closest = from_palette
        result.append(closest)
        closest = to_array(closest)
        palette.append(closest[0])
        palette.append(closest[1])
        palette.append(closest[2])

    print_theme(sorted(result, key=luminance), "closest", block_size=3)

    p_img = Image.new('P', (1, 1))
    p_img.putpalette(palette)

    p = image.quantize(palette=p_img, kmeans=4, dither=0).convert('RGB')

    return p
