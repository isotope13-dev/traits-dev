package main

import "os/exec"

// Runtime inventory token, not a privilege escalation: execRschedsudog
// juxtaposes the os/exec package path with the scheduler wait-queue struct.
// The guard matcher must not read this as a command invocation.
var _ = exec.Command
