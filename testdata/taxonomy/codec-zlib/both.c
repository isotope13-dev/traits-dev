#include <zlib.h>
int main(void) {
    z_stream stream = {0};
    int compressed = deflate(&stream, Z_FINISH);
    int expanded = inflate(&stream, Z_NO_FLUSH);
    return compressed + expanded;
}
