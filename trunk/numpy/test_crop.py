import crop
import numpy

a = numpy.zeros((5,10),numpy.int)
a[numpy.arange(5),:] = numpy.arange(10)

b = numpy.transpose([(10 ** numpy.arange(5))])
a = (a*b)[:,1:] #this array is most likely NOT contiguous

print a
print "dim1=%d dim2=%d" % (a.shape[0],a.shape[1])

d1_0 = 2
d1_1 = 4
d2_0 = 1
d2_1 = 5

c = crop.crop(a, d1_0,d1_1, d2_0,d2_1)
d = a[d1_0:d1_1, d2_0:d2_1]

print "returned array:"
print c

print "native slicing:"
print d


