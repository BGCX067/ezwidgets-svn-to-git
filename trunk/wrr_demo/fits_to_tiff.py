import pyfits
import numpy
from libtiff import TIFFimage
import Image
import sys
import math
import os

#http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html
def histeq(im,nbr_bins=256):
    #get image histogram
    imhist,bins = numpy.histogram(im.flatten(),nbr_bins,normed=True)
    cdf = imhist.cumsum() #cumulative distribution function
    cdf = 255 * cdf / cdf[-1] #normalize

    #use linear interpolation of cdf to find new pixel values
    im2 = numpy.interp(im.flatten(),bins[:-1],cdf).astype(numpy.uint8)

    return im2.reshape(im.shape), cdf

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Need a filename..."
        sys.exit(1)

    fn = sys.argv[1]
    f = pyfits.open(fn)

    #will need the fn without extension later...
    fn,_ = os.path.splitext(fn)

    hdu = f[0]
    bitpix = hdu.header['bitpix']
    bzero = hdu.header['bzero']

    #is the image flipped? No worries!
    d = hdu.data[::-1,:]

    #removing mask (if I understood this bit of the spec correctly)
    d[d<bzero] = bzero

    mi = numpy.min(d)
    ma = numpy.max(d)
    print d.shape, d.dtype,mi,ma

    #mostly, we want 16 bit images...
    if bitpix != 16:
        d = 65535*(d - mi)/(ma-mi)

    print "writing 16 bit tiff..."
    d16 = d.astype(numpy.uint16)
    tiff = TIFFimage(d16,
        description='http://tdc-www.harvard.edu/postage_stamp/')
    tiff.write_file(fn+'.tif', compression='lzw')
    #flush the file to disk:
    del tiff

    print "writing equalized 8 bit png and jpeg..."
    d8,cdf = histeq(d,65536)
    i = Image.fromarray(d8)
    i.save(fn+'.png')
    i.save(fn+'.jpg')

