import inplace
import numpy

a = numpy.array([1,2,3],'d')
print a
inplace.inplace(a)
print a
