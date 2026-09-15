package imagefixture

import (
	"os/exec"
	"strings"
)

// Reassignment, not the earlier query, determines the output destination.
func imageAfterQuery() *exec.Cmd {
	out, _ := exec.Command("findmnt", "-no", "SOURCE", "/").Output()
	target := strings.TrimSpace(string(out))
	target = "/tmp/image-fixture.bin"
	return exec.Command("dd", "if=/dev/zero", "of="+target, "bs=446", "count=1")
}
