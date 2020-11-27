import pathlib

from setuptools import setup

setup(name='mola',
      version='0.1.0',
      author='xmonarch',
      author_email='xmonarch64@gmail.com',
      packages=['mola'],
      scripts=['bin/mola'],
      description="Tool for coloring images according to a defined color theme",
      long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
      long_description_content_type="text/markdown",
      install_requires=['argparse', 'scikit-image', 'numpy', 'colour', 'Pillow'],
      license="GPLv2",
      platforms=["Independent"],
      keywords="image process colorize",
      url="https://github.com/xmonarch/mola",
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.8",
      ]
      )
