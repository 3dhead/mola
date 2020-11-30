# mola

Tool for coloring images according to a defined color theme. Provides a wrapper for `feh` as well as definitions
of common terminal themes to allow user to quickly set any wallpaper matching the terminal colors.

## Results

### Original Image

![Original](/images/original.jpg)

By [ALEXANDRE DINAUT](https://unsplash.com/@alexdinaut) available [here](https://unsplash.com/photos/zqxnyb7M5kI)

In all cases the image has been processing with 50% precision. 

### nord

Regular:

![nord](/images/nord.jpg)

Aggressive:

![nord_aggressive](/images/nord_a.jpg)

### gruvbox

Regular:

![gruvbox](/images/gruvbox.jpg)

Aggressive:

![gruvbox_aggressive](/images/gruvbox_a.jpg)

### mocha

Regular:

![mocha](/images/mocha.jpg)

Aggressive:

![mocha_aggressive](/images/mocha_a.jpg)

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
- `ashes` (source: https://terminal.sexy/)
- `gruvbox` (source: https://github.com/morhetz/gruvbox)
- `mocha` (source: https://terminal.sexy/)
- `monokai` (source: https://terminal.sexy/)
- `nord` (source: https://www.nordtheme.com/)
- `ocean` (source: https://terminal.sexy/)
- `tomorrow` (source: https://terminal.sexy/)
- `twilight` (source: https://terminal.sexy/)

More to follow... Contributions are welcome.

## Issues and limitations
- Performance is still far from optimal. Processing large images with high precision can sometimes take > 20s, which needs to be improved
- In general JPEG compression artifacts don't play well with histogram matching algorithm - results of processing highly compressed images will most likely not be satisfactory 
- At the moment `mola` depends on both `Pillow` and `scikit-image` - hopefully one of those will be removed  
