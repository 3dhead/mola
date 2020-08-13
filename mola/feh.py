import subprocess
import tempfile
from typing import List

from mola.colorize import colorize


def feh(params, additional_params: List):
    """
    Colorize input image and set as wallpaper with feh
    :param params: CLI arguments
    :param additional_params: CLI arguments to be passed to feh
    """
    with tempfile.NamedTemporaryFile(suffix=".jpg") as temp:
        """
        Using a temporary file for colorizer output
        """
        params.output_file = temp.name

        """
        Colorize input image
        """
        colorize(params)

        """
        Pass the output along with additional CLI arguments to feh
        """
        subprocess.run(["feh"] + additional_params + [params.output_file])
