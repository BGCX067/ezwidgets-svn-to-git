import numpy
import wrr
import Image
import time

nbits = 16
BlurStdDev = 100.0
WeightStdDev = 20.0
Radius = 20
Step = 1
max_level = 2**nbits-1

print "loading"
img = Image.open("wpix.tif")
img.load()
arr = numpy.array(img.getdata()).reshape(img.size[::-1]).astype('i')

for Radius in [5,10,20,40]:
    print "Radius %d:"%Radius,

    t = time.time()
    #a = wrr.parallel_wrr(arr,8,BlurStdDev,WeightStdDev,Radius,Step)
    a = wrr.wrr(arr,8,BlurStdDev,WeightStdDev,Radius,Step)
    print "took %.2fs" % (time.time()-t)

    print numpy.min(a), numpy.max(a)

    i = Image.fromarray(a.astype(numpy.uint8))
    i.save("test_wrr_%d.png" % Radius)
