import rev
import revnum

import time
import numpy

#loop a 1000 times, string is 5MB.
x = 1001
s = "Hello"*1024*1024
arr = numpy.fromstring(s,numpy.uint8)

t = time.time()
for i in range(x):
    s2 = rev.reverse(s)

print "string version: %d times took %.2f seconds" % (x,time.time()-t)
print s2[:10]

t = time.time()
for i in range(x):
    s2 = revnum.reverse(arr)

print "numpy version: %d times took %.2f seconds" % (x,time.time()-t)
print s2[:10].tostring()

t = time.time()
for i in range(x):
    revnum.inplace(arr)

print "inplace version: %d times took %.2f seconds" % (x,time.time()-t)
print arr[:10].tostring()
