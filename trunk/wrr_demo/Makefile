IDIR =.
CC=gcc
CFLAGS=-I$(IDIR) -march=native -O9 -ffast-math -fopenmp

ODIR=obj

LIBS=-lm -lgomp -lrt

_DEPS = wrr.h myalloc.h gopt.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = test_wrr.o wrr.o myalloc.o  gopt.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

test_wrr: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 
