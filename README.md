# python-halftone

A python module that uses [Pillow][pillow] to give images a halftone effect.

It is adapted from [this StackOverflow answer][so] (which includes example images) by [fraxel][fr].

[pillow]: http://pillow.readthedocs.io
[so]: http://stackoverflow.com/questions/10572274/halftone-images-in-python/10575940#10575940
[fr]: http://stackoverflow.com/users/1175101/fraxel

Running it over large images, or with settings that create large images, can take some time.

## Basic usage

    import halftone
    h = halftone.Halftone('/path/to/myimage.jpg')
    h.make()

Will create a new image at `/path/to/myimage_halftoned.jpg`, using the default settings.

## Options
There are a number of options that can be added to the `make()` call, e.g.:

	h.make(filename_addition='_new', scale=2)

The full list of options:

### `angles`

A list of 4 angles, in degrees, that each channel should be rotated by. If `style='grayscale'` only the first angle is used. Experimenting with different angles can increase or reduce moiré patterns.

Default: `[0,15,30,45]`

### `antialias`

A boolean value, indicating whether the circles drawn should be antialiased. Because Pillow doesn't draw antialias shapes, this is done by drawing the image at 4x the size and then reducing it to the desired size, antialiasing as part of the process.

Default: `False`

### `filename_addition`

When saving the new image, this string will be added to the original filename. e.g. if the original filename is `puppy.jpg` and `filename_addition='_halftoned'`, the saved file will be `puppy_halftoned.jpg`.

Default: `"_halftoned"`

### `percentage`

How much of the gray component to remove from the CMY channels and put in the K channel.

Default: `0`

### `sample`

When creating each circle in the new image, what area of pixels should that circle represent?

Default: `10`

### `scale`

Scale of the output image. The maximum output dot diameter is `sample * scale` (which is also the number of possible dot sizes).

Default `1`

### `style`

Either `'color'` or `'grayscale'`. For color, four screens are output, one each for cyan, magenta, yellow and black. For grayscale, only black dots are generated, only the first number in the `angles` list is used, and the `percentage` value is ignored.

Default: `'color'`

## Examples

An example of `make()` using all options:

	h.make(
		angles=[108, 162, 90, 45],
		antialias=True,
		filename_addition='_new',
		percentage=50,
		sample=5,
		scale=2,
		style='color'
	)
