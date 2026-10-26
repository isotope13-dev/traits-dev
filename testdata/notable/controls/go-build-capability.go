package builder
import "os/exec"
func build() {
    cmd := exec.Command("go", "build", "-o", "output", ".")
    _ = cmd.Run()
}
