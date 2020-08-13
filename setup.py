import pathlib

from setuptools import setup

setup(name='mola',
      version='0.1.0',
      author='xmonarch',
      author_email='xmonarch64@gmail.com',
      packages=['mola'],
      scripts=['bin/mola'],
      description="Automatically adjust image colors to a given color palette",
      long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
      long_description_content_type="text/markdown",
      install_requires=['argparse', 'scikit-image', 'numpy', 'colour'],
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