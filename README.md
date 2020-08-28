# mola

Tool for coloring images according to a defined color theme. Provides a wrapper for `feh` as well as definitions
of common terminal themes to allow user to quickly set any wallpaper matching the terminal colors.

## Usage

In order to list existing color themes: 
```shell
$ mola -l
```

If your terminal support true color you can also preview themes with:
```shell
$ mola -v -l
```

Colorize input image using a nord theme and store the result in a file:
```shell
$ mola -t nord input.jpg output.jpg
```
Colorize input image using a nord theme and set as wallpaper using `feh`:
```shell
$ mola -t nord input.jpg
```

Previous command defaults to `--bg-scale` attribute in `feh`, however other options can also be passed as parameter to `mola`:
```shell
$ mola -t nord input.jpg --bg-fill
```

To specify colors manually instead of using a theme:
```shell
$ mola -c #fff -c #e3e3e3 -c #d5d5d5 -c #ffff00 input.jpg --bg-center
```

You can also combine a theme with additional colors as in:
```shell
$ mola -t gruvebox -c #e3e3e3 -c #d5d5d5 -c #ffff00 input.jpg --bg-scale
```

To enable verbose logs use the `-v` option.

## Results

## Features

## Installation

```shell
$ git clone https://github.com/xmonarch/mola.git
```

```shell
$ cd mola
```

```shell
$ sudo pip install .
```

## Examples
