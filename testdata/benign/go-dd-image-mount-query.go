package imagefixture

import (
	"os"
	"os/exec"
	"strings"
)

// Mount diagnostics and an image-file command have unrelated destinations.
// This fixture is inspected statically; no image command is started.
func imageWithMountDiagnostics() *exec.Cmd {
	data, _ := os.ReadFile("/proc/mounts")
	_ = strings.Contains(string(data), "/dev/")
	out, _ := exec.Command("findmnt", "-no", "SOURCE", "/").Output()
	_ = strings.TrimSpace(string(out))
	return exec.Command("dd", "if=/dev/zero", "of=/tmp/image-fixture.bin", "bs=446", "count=1")
}
