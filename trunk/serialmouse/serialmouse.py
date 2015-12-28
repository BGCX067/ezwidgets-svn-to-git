import serial

def init(timeout=0.5):
    ser = serial.Serial(0)  #open first serial port
    ser.baudrate = 1200
    ser.bytesize = serial.SEVENBITS
    ser.parity=serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout=timeout
    ser.xonxoff=0
    ser.rtscts=0
    ser.open()
    g=ser.read(30)

    return ser

def tobin(val):
    retret=[]
    for c in val:
        value=ord(c)
        ret=[]
        for i in range(8):
            a=pow(2,i)
            ret.append((value & a)>0)
        retret.append(ret)

    return retret

def read(ser,verbose=0):
    g=ser.read(1)

    if g=='':
        return None

    while ord(g) & 64 == 0:
        g=ser.read(1)
        
    g=g+ser.read(2)

    if len(g)==3:
        vals=tobin(g)
        l=vals[0][5]
        r=vals[0][4]
        x=vals[0][1]*-128+vals[0][0]*64+vals[1][5]*32+vals[1][4]*16+vals[1][3]*8+vals[1][2]*4+vals[1][1]*2+vals[1][0]
        y=vals[0][3]*-128+vals[0][2]*64+vals[2][5]*32+vals[2][4]*16+vals[2][3]*8+vals[2][2]*4+vals[2][1]*2+vals[2][0]

        if verbose == 1:
            print "L:%d R:%d X:%d Y:%d" % (l,r,x,y)
        return x,y,l,r
    else:
        return None

def flush(ser):
    ser.flush()

if __name__ == '__main__':
    #init the com port
    ser=init()

    #read and print
    while 1:
        read(verbose=1)
