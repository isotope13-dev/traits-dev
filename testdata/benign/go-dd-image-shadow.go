package imagefixture

import (
	"os/exec"
	"strings"
)

func queriedSource() string {
	out, _ := exec.Command("findmnt", "-no", "SOURCE", "/").Output()
	return strings.TrimSpace(string(out))
}

// The if initializer's target is not the target used after the if statement.
func imageAfterScopedQuery() *exec.Cmd {
	target := "/tmp/image-fixture.bin"
	if target := queriedSource(); target != "" {
		_ = target
	}
	return exec.Command("dd", "if=/dev/zero", "of="+target, "bs=446", "count=1")
}
