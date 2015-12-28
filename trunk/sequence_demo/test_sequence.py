import cv2
import numpy
import mytest
import sys
import time

niter = 5
max_count = 50

if __name__ == '__main__':
    fn = r"e:\ATM.mpg"
    vidcap = cv2.VideoCapture(fn)

    count = 0
    stack = []

    success,image = vidcap.read()
    if success:
        while success:
            stack.append(mytest.grayscale(image))
            count += 1

            success,image = vidcap.read()
            if count >= max_count:
                break

    if count == 0:
        sys.exit(1)

    height,width,_ = image.shape
    print "loaded %d (h%d x w%d) frames" % (count,height,width)

    if 1:
        print "testing mytest average..."

        tt = 0
        for i in range(niter):
            t = time.time()
            b = mytest.average(stack)
            tt += (time.time()-t)

        print "  mytest average took %.2f seconds, sum=%d" % (tt/niter,numpy.sum(b.astype(int)))

    if 1:
        print "\ntesting numpy.average",

        tt = 0
        for i in range(niter):
            print ".",
            t = time.time()
            b = numpy.mean(numpy.array(stack,float),axis=0).astype(numpy.uint8)
            tt += (time.time()-t)

        print "\n  numpy.mean took %.2f seconds, sum=%d" % (tt/niter,numpy.sum(b.astype(int)))

    if 1:
        print "\ntesting inplace background subtraction..."

        tt = 0
        t = time.time()
        mytest.bsub(stack,b)
        tt += (time.time()-t)

        print "  bsub took %.2f seconds (inplace op, done once)" % tt

    if 1:
        print "\nsaving images..."
        fn = "test_bg.png"
        cv2.imwrite(fn,b)
        for i in range(count):
            fn = "test_%05d.png" % i
            cv2.imwrite(fn,stack[i])


