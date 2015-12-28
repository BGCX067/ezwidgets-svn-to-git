import atexit
import numpy
print "first message is from __call_at_begining()"
import ezview

#There is no easy way to finalize the module (see PEP3121)
atexit.register(ezview.finalize)

a = ezview.set_ones()
print "\ncalling ezview.set_ones() - now the memory block is all ones.\nReturned array (a view on the allocated memory block) is:"
print a

print "\nwe're setting the array using a[:]=arange(a.shape[0])\nThis changes the content of the allocated memory block:"
a[:] = numpy.arange(a.shape[0])
print a

print "\nwe're now deleting the array  - this only deletes the view,\nnot the allocated memory!"
del a

print "\nlet's get a new view on the allocated memory, should STILL contain [0,1,2,3...]"
b = ezview.get_view()
print b

print "\nnext message from __call_at_end() - finalize() registered via module atexit"
