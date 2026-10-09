#include <strings.h>
int compare_frames(const char **frames, unsigned count) {
    unsigned same = 0;
    for (unsigned i = 1; i < count; ++i) {
        if (bcmp(frames[0], frames[i], 8)) continue;
        ++same;
    }
    return same;
}
