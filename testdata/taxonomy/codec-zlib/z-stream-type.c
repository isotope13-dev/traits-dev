#include <zlib.h>
int main(void) {
    z_stream stream = {0};
    return (int)stream.total_in;
}
