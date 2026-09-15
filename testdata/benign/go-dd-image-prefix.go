package imagefixture

import "os/exec"

// An image-builder command targeting an ordinary disposable file, not a device.
func imagePrefix() *exec.Cmd {
	return exec.Command("dd", "if=/dev/zero", "of=/tmp/image-fixture.bin", "bs=446", "count=1")
}
