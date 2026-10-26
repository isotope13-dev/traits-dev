// Near-miss control: an ordinary CLI (SBOM-emitter shape) carrying a bare
// --output-format flag with no masscan-specific marker anywhere. The neutral
// option atom must fire; the masscan composite must stay silent.
#if defined(__APPLE__)
#define TEXT_SECTION __attribute__((section("__TEXT,.text")))
#else
#define TEXT_SECTION __attribute__((section(".text")))
#endif

static const char flags[] TEXT_SECTION =
    "sbom-tool --output-format cyclonedx-json --output sbom.json";

int main(int argc, char **argv) {
    return (int)(flags[argc] + argv[0][0]);
}
