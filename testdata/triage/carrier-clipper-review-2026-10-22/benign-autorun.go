// An explicit --install example. These bytes are compiled and scanned only.
package main

import (
    "fmt"
    "os"
    "os/exec"
    "path/filepath"
)

func scheduled() {
    image, _ := os.Executable()
    _ = exec.Command("schtasks", "/create", "/tn", "ExampleTask", "/tr", image,
        "/sc", "hourly", "/st", "00:00", "/f").Run()
}

func startup() {
    dir := filepath.Join(os.Getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    image, _ := os.Executable()
    target := filepath.Join(dir, "Example.lnk")
    command := fmt.Sprintf(`$s = New-Object -comObject WScript.Shell
$c = $s.CreateShortcut("%s")
$c.TargetPath = "%s"
$c.Save()`, target, image)
    _ = exec.Command("powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", command).Run()
}

func main() {
    if len(os.Args) > 1 && os.Args[1] == "--install" {
        scheduled()
        startup()
    }
}
