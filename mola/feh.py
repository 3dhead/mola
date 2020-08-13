import logging
import subprocess
import tempfile
import time
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

        """
        Using a temporary file for colorizer output
        """
        params.output_file = temp.name
        LOG.debug(f"Using temporary path '{params.output_file}'")

        """
        Colorize input image
        """
        colorize(params)

        """
        Pass the output along with additional CLI arguments to feh
        """
        now = time.time()
        LOG.info("Running feh...")
        # TODO log arguments
        subprocess.run(["feh"] + additional_params + [params.output_file])
        LOG.debug("Done in {:.2f}s".format(time.time() - now))
