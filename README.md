# python-halftone

A python module that uses [Pillow][pillow] to give images a halftone effect.

It is adapted from [this StackOverflow answer][so] (which includes example images) by [fraxel][fr].

[pillow]: http://pillow.readthedocs.io
[so]: http://stackoverflow.com/questions/10572274/halftone-images-in-python/10575940#10575940
[fr]: http://stackoverflow.com/users/1175101/fraxel


## Usage

    import halftone
    h = halftone.Halftone('/path/to/myimage.jpg')
    h.make(filename_addition='_halftoned')

Will create a new image at `/path/to/myimage_halftoned.jpg`, halftoned with the
default settings.

The full list of options:

* `filename_addition`: What to add to the filename (before the extension) (default ``).
* `sample`: Sample box size from original image, in pixels (default `10`).
* `scale`: Max output dot diameter is `sample * scale` (which is also the number of possible dot sizes) (default `1`).
* `percentage`: How much of the gray component to remove from the CMY channels and put in the K channel (default `0`).
* `angles`: A list of 4 angles that each screen channel should be rotated by (default `[0,15,30,45,]`).
* `style`: Either `color` or `grayscale`. For grayscale, only black dots are generated, only the first number in the `angles` array is used, and the `percentage` value is ignored. (default: 'color').


An example of `make()` using all options:

	h.make(
		filename_addition='_dotty',
		sample=5,
		scale=1,
		percentage=50,
		angles[108, 162, 90, 45],
        style='color',
	)

Running it over large images, or with settings that create large images, can take some time.
