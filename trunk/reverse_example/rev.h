typedef struct binary_data {
    size_t size;
    unsigned char* data;
} binary_data;

void reverse(unsigned char *s_in, size_t size_in, unsigned char **s_out, size_t *size_out);
binary_data revstruct(unsigned char *s_in, size_t size_in);

