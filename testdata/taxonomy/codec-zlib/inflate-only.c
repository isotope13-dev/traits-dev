#include <zlib.h>
int main(void) {
    z_stream stream = {0};
    return inflate(&stream, Z_NO_FLUSH);
}
