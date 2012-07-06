try:
    import Image, ImageDraw, ImageStat
except ImportError, e:

    try:
        import PIL.Image as Image
        import PIL.ImageDraw as ImageDraw
        import PIL.ImageStat as ImageStat
    except:
        raise
except:
    raise

import os, sys

"""
Class: Halftone( path )
Usage: 
    import halftone
    h = halftone.Halftone('/path/to/image.jpg')
    h.make(filename_addition='_halftoned')

The bulk of this is taken from this Stack Overflow answer by fraxel:
http://stackoverflow.com/a/10575940/250962
"""

class Halftone(object):
    def __init__(self, path):
        """
        path is the path to the image we want to halftone.
        """
        self.path = path

    def make(self, sample=10, scale=1, percentage=0, filename_addition='', angles=[0,15,30,45]):
        """
        Leave filename_addition empty to save the image in place.
        Arguments:
            sample: Sample box size from original image, in pixels.
            scale: Max output dot diameter is sample * scale (which is also the 
                number of possible dot sizes)
            percentage: How much of the gray component to remove from the CMY 
                channels and put in the K channel.
            filename_addition: What to add to the filename (before the extension).
            angles: A list of 4 angles that each screen channel should be rotated by.
        """
        f, e = os.path.splitext(self.path)
        outfile = "%s%s%s" % (f, filename_addition, e)
        try:
            im = Image.open(self.path)
        except IOError:
            print "Cannot open ", self.path

        cmyk = self.gcr(im, percentage)
        dots = self.halftone(im, cmyk, sample, scale, angles)
        new = Image.merge('CMYK', dots)
        new.save(outfile)


    def gcr(self, im, percentage):
        """
        Basic "Gray Component Replacement" function. Returns a CMYK image with 
        percentage gray component removed from the CMY channels and put in the
        K channel, ie. for percentage=100, (41, 100, 255, 0) >> (0, 59, 214, 41)
        """
        cmyk_im = im.convert('CMYK')
        if not percentage:
            return cmyk_im
        cmyk_im = cmyk_im.split()
        cmyk = []
        for i in xrange(4):
            cmyk.append(cmyk_im[i].load())
        for x in xrange(im.size[0]):
            for y in xrange(im.size[1]):
                gray = min(cmyk[0][x,y], cmyk[1][x,y], cmyk[2][x,y]) * percentage / 100
                for i in xrange(3):
                    cmyk[i][x,y] = cmyk[i][x,y] - gray
                cmyk[3][x,y] = gray
        return Image.merge('CMYK', cmyk_im)


    def halftone(self, im, cmyk, sample, scale, angles):
        '''Returns list of half-tone images for cmyk image. sample (pixels), 
           determines the sample box size from the original image. The maximum 
           output dot diameter is given by sample * scale (which is also the number 
           of possible dot sizes). So sample=1 will presevere the original image 
           resolution, but scale must be >1 to allow variation in dot size.'''
        cmyk = cmyk.split()
        dots = []
        for channel, angle in zip(cmyk, angles):
            channel = channel.rotate(angle, expand=1)
            size = channel.size[0]*scale, channel.size[1]*scale
            half_tone = Image.new('L', size)
            draw = ImageDraw.Draw(half_tone)
            for x in xrange(0, channel.size[0], sample):
                for y in xrange(0, channel.size[1], sample):
                    box = channel.crop((x, y, x + sample, y + sample))
                    stat = ImageStat.Stat(box)
                    diameter = (stat.mean[0] / 255)**0.5
                    edge = 0.5*(1-diameter)
                    x_pos, y_pos = (x+edge)*scale, (y+edge)*scale
                    box_edge = sample*diameter*scale
                    draw.ellipse((x_pos, y_pos, x_pos + box_edge, y_pos + box_edge), fill=255)
            half_tone = half_tone.rotate(-angle, expand=1)
            width_half, height_half = half_tone.size
            xx=(width_half-im.size[0]*scale) / 2
            yy=(height_half-im.size[1]*scale) / 2
            half_tone = half_tone.crop((xx, yy, xx + im.size[0]*scale, yy + im.size[1]*scale))
            dots.append(half_tone)
        return dots

if __name__ == '__main__': 

    import sys
    import halftone

    path = sys.argv[1]

    h = Halftone(path)
    h.make(filename_addition='_halftoned')

