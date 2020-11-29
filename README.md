# mola

Tool for coloring images according to a defined color theme. Provides a wrapper for `feh` as well as definitions
of common terminal themes to allow user to quickly set any wallpaper matching the terminal colors.

## Results

## Usage

Colorize input image using a nord theme and store the result in a file:
```shell
$ mola -t nord -o output.jpg input.jpg
```

Colorize input image using a nord theme and set as wallpaper using `feh`:
```shell
$ mola -t nord --bg-fill input.jpg
```

To specify colors manually instead of using a theme:
```shell
$ mola -c "#fff" -c "#e3e3e3" -c "#d5d5d5" -c "#ffff00" --bg-center input.jpg
```

You can also combine a theme with additional colors as in:
```shell
$ mola -t gruvbox -c "#e3e3e3" -c "#d5d5d5" -c "#ffff00" --bg-scale input.jpg
```

The theme colors can be also be retrieved from any file containing HEX colors by using `-f` option instead of `-t` for example:
```shell
$ mola -f ~/.config/termite/config --bg-scale input.jpg
```

If the processing is taking too long it's possible to control the coloring precision by using the `-p` flag, 
however the results will be less accurate:  
```shell
$ mola -t nord -p 50 input.jpg
```

To enable verbose logs use the `-v` option.

## Installation

```shell
$ git clone https://github.com/xmonarch/mola.git
$ cd mola
$ sudo pip install .
```

## Themes

Currently included themes:
- `gruvbox` (credit: https://github.com/morhetz/gruvbox)
- `nord` (credit: https://www.nordtheme.com/)

More to follow... Contributions are welcome.

## Issues and limitations
- Performance
- Artifacts
- In general JPEG compression artifacts don't play well with histogram matching algorithm - results of processing highly compressed images will most likely not be satisfactory 
- At the moment `mola` depends on both `Pillow` and `scikit-image` - hopefully one of those will be removed  
