// Positive control: a masscan-family binary shape. The --output-format flag
// sits beside masscan-specific markers (tool name, distinctive options,
// scan banner), so the anchored composite must fire. Markers live in .text
// (as in real scanner builds, where option bytes are code immediates),
// because the masscan option atoms are section-scoped to .text.
#if defined(__APPLE__)
#define TEXT_SECTION __attribute__((section("__TEXT,.text")))
#else
#define TEXT_SECTION __attribute__((section(".text")))
#endif

static const char flags[] TEXT_SECTION =
    "masscan --output-format xml --randomize-hosts --adapter-ip 10.0.0.1";
static const char banner[] TEXT_SECTION =
    "# Masscan 1.0.6 scan initiated";

int main(int argc, char **argv) {
    return (int)(flags[argc] + banner[argc] + argv[0][0]);
}
