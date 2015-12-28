#!python

import traceback,sys
import numpy
import ezerr

print "\n--- testing ezerr.val() ---"
a = numpy.arange(10)
indexes = [5,20,-1]

for i in indexes:
    try:
        value = ezerr.val(a,i)
    except:
        print ">> failed for index=%d" % i
        traceback.print_exc(file=sys.stdout)
    else:
        print "using ezerr.val() a[%d]=%d - should be %d" % (i,value,a[i])

print "\n--- testing ezerr.alloc() ---"
amounts = [1,-1] #1 byte, -1 byte

for n in amounts:
    try:
        ezerr.alloc(n)
    except:
        print ">> could not allocate %d bytes" % n
        traceback.print_exc(file=sys.stdout)
    else:
        print "allocated (and deallocated) %d bytes" % n

