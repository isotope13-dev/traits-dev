#include <zlib.h>
int main(void) {
    z_stream stream = {0};
    return deflate(&stream, Z_FINISH);
}
