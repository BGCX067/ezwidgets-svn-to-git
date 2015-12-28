import ezalloc

n = 2048

# this multiplied by sizeof(int) to get size in bytes...
#assuming sizeof(int)=4 on a 32bit machine (sorry, it's late!)
m = 1024 * 1024
err = 0

print "ARGOUTVIEWM_ARRAY1 (managed arrays) - %d allocations (%d bytes each)" % (n,4*m)
for i in range(n):
    try:
        #allocating some memory
        a = ezalloc.alloc_managed(m)
        #deleting the array
        del a
    except:
        err = 1
        print "Step %d failed" % i
        break

if err == 0:
    print "Done!\n"

print "ARGOUTVIEW_ARRAY1 (unmanaged, leaking) - %d allocations (%d bytes each)" % (n,4*m)
for i in range(n):
    try:
        #allocating some memory
        a = ezalloc.alloc_leaking(m)
        #deleting the array
        del a
    except:
        err = 1
        print "Step %d failed" % i
        break

if err == 0:
    print "Done? Increase n!\n"
