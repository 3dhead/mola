import logging
import subprocess
import tempfile
from typing import List

from mola.colorize import colorize

LOG = logging.getLogger(__name__)


def feh(params, additional_params: List):
    """
    Colorize input image and set as wallpaper with feh
    :param params: CLI arguments
    :param additional_params: CLI arguments to be passed to feh
    """
    with tempfile.NamedTemporaryFile(suffix=".jpg") as temp:
        # using a temporary file for colorizer output
        params.output_file = temp.name
        LOG.debug(f"Using temporary path '{params.output_file}'")

        # colorize input image
        colorize(params)

        # pass the output along with additional CLI arguments to feh
        LOG.info("Running feh...")
        feh_attributes = additional_params + [params.output_file]
        LOG.debug(f"feh attributes: {feh_attributes}")
        subprocess.run(["feh"] + feh_attributes)
