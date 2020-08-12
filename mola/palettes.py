from typing import List, Dict

from colour import Color


def of(colors: List[str]) -> List[Color]:
    """
    Convert list of HEX color representations into a list of color objects
    :param colors: list of HEX colors for a palette
    :return: list of colour.Color object
    """
    return [Color(color_hex) for color_hex in colors]


"""
List of known color palettes
"""
PALETTES: Dict[str, List[Color]] = dict()

"""
See https://www.nordtheme.com/
"""
PALETTES['nord'] = of(
    ['#2e3440', '#3b4252', '#434c5e', '#4c566a', '#d8dee9', '#e5e9f0', '#eceff4', '#8fbcbb', '#88c0d0', '#81a1c1',
     '#5e81ac', '#bf616a', '#d08770', '#ebcb8b', '#a3be8c', '#b48ead'])
