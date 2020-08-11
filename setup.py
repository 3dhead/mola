import pathlib

from setuptools import setup

setup(name='mola',
      version='0.1.0',
      author='xmonarch',
      author_email='xmonarch64@gmail.com',
      packages=['mola'],
      scripts=['bin/mola'],
      description="Automatically adjust wallpaper colors to your terminal palette",
      long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
      long_description_content_type="text/markdown",
      install_requires=['argparse', 'pillow', 'colour'],
      license="GPLv2",
      platforms=["Independent"],
      keywords="",
      url="https://github.com/xmonarch/mola",
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.8",
      ]
      )
