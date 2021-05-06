# python-halftone

A Python 3 module that uses [Pillow][pillow] to give images a halftone effect (see below for examples).

It is adapted from [this StackOverflow answer][so] (which includes example images) by [fraxel][fr].

Running it over large images, or with settings that create large images, can take some time.

Also see [Clay Flannigan's halftone][clay] in case that suits your needs better.

[pillow]: http://pillow.readthedocs.io
[so]: http://stackoverflow.com/questions/10572274/halftone-images-in-python/10575940#10575940
[fr]: http://stackoverflow.com/users/1175101/fraxel
[clay]: https://github.com/ClayFlannigan/halftone

## Basic usage

```python
import halftone

h = halftone.Halftone("/path/to/myimage.jpg")
h.make()
```

Will create a new image at `/path/to/myimage_halftoned.jpg`, using the default settings.

## Options

There are a number of options that can be added to the `make()` call, e.g.:

```python
h.make(filename_addition="_new", scale=2)
```

The full list of options:

### `angles`

A list of 4 angles, in degrees, that each channel (CMYK, in that order) should be rotated by. If `style="grayscale"` only the first angle is used. Experimenting with different angles can increase or reduce moiré patterns. [More on screen angles.](http://the-print-guide.blogspot.co.uk/2009/05/halftone-screen-angles.html)

Default: `[0, 15, 30, 45]`

### `antialias`

A boolean value, indicating whether the circles drawn should be antialiased. Because Pillow doesn't draw antialias shapes, this is done by drawing the image at 4x the size and then reducing it to the desired size, antialiasing as part of the process.

Default: `False`

### `filename_addition`

When saving the new image, this string will be added to the original filename. e.g. if the original filename is `"puppy.jpg"` and `filename_addition="_new"`, the saved file will be `"puppy_new.jpg"`.

Default: `"_halftoned"`

### `percentage`

How much of the gray component to remove from the CMY channels and put in the K channel.

Default: `0`

### `sample`

When creating each circle in the new image, what area of pixels should that circle represent?

Default: `10`

### `save_channels`

Whether to save the four CMYK channels as separate images, in addition to the combined halftoned image. Boolean. The files will have the color letter appended to the filename, like `puppy_halftoned_c.jpg` for the cyan channel. Only functions if the overall `style` argument is `"color"`.

Default: `False`

### `save_channels_format`

Either `"default"`, `"jpeg"`, or `"png"`. If `save_channels` is `True` then what format should the four separate images be saved as? If `"default"` then it's the same as the original input image's format.

Default: `"default"`

### `save_channels_style`

Either `"color"` or `"grayscale"`. If `save_channels` is `True` then whether the four separate images should be saved in color or grayscale. If the overall `style` argument is `"grayscale"` then the four CMYK channels will always be `"grayscale"`, no matter what this setting.

Default: `"color"`

### `scale`

Scale of the output image. The maximum output dot diameter is `sample * scale` (which is also the number of possible dot sizes).

Default `1`

### `style`

Either `"color"` or `"grayscale"`. For color, four screens are output, one each for cyan, magenta, yellow and black. For grayscale, only black dots are generated, only the first number in the `angles` list is used, and the `percentage` value is ignored.

Default: `"color"`

## Examples

An example of `make()` using all options:

```python
h.make(
    angles=[15, 75, 0, 45],
    antialias=True,
    filename_addition="_new",
    percentage=50,
    sample=5,
    save_channels=True,
    save_channels_format="png",
    save_channels_style="grayscale",
    scale=2,
    style="color"
)
```

See the `examples/` directory for the example images below.

### Original image

![Original image of dog](examples/original.jpg?raw=True)

Other than the `filename_addition` option, the images below have been created
using the options specified.

### Default settings

```python
h.make()
```

![Original image of dog](examples/defaults.jpg?raw=True)

### Custom screen angles

Using different screen angles to reduce moiré (but resulting in a different pattern).

```python
h.make(angles=[15, 45, 0, 75])
```

![Image of dog with custom screen angles](examples/angles.jpg?raw=True)

### Smaller sample

Reducing the sample size and increasing the scale (to increase output detail).

```python
im.make(sample=5, scale=2)
```

![Image of dog with smaller sample size](examples/sample_scale.jpg?raw=True)

### Antialias

With antialiased circles.

```python
im.make(antialias=True)
```

![Antialiased image of dog](examples/antialiased.jpg?raw=True)

### Grayscale

Black and white, setting the angle to 45 (the default angle would be 0, resulting in circles being in rows and columns).

```python
im.make(style="grayscale", angles=[45])
```

![Grayscale image of dog](examples/grayscale.jpg?raw=True)
