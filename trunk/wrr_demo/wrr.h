void wrr(int *ImageIn, int Ydim, int Xdim, int nbits, float BlurStdDev, float WeightStdDev, int Radius, int Step, int **ImageOut, int *YdimOut, int *XdimOut);
void parallel_wrr(int *ImageIn, int Ydim, int Xdim, int nbits, float BlurStdDev, float WeightStdDev, int Radius, int Step, int **ImageOut, int *YdimOut, int *XdimOut);
void rr(int *ImageIn, int Ydim, int Xdim, int nbits, int Radius, int Step, int **ImageOut, int *YdimOut, int *XdimOut);
void parallel_rr(int *ImageIn, int Ydim, int Xdim, int nbits, int Radius, int Step, int **ImageOut, int *YdimOut, int *XdimOut);

