// Python C-extension entry-stub shape: a single PyInit export forwarding to
// the real implementation library (cf. torch/_C*.so fronting
// libtorch_python). The padding keeps the image above the low-string-count
// size floors without adding strings: tens of KB with a handful of strings
// and imports is the whole file, not a concealed table.
#include <stdint.h>
static uint8_t image_pad[60000] = {1};
void *PyInit__controls(void) { return (void *)image_pad; }
