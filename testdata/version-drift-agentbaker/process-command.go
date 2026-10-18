package fixture

import "os/exec"

func main() {
    exec.Command("sh", "-c", "printf ready").Run()
}
