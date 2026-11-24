package queries
import "os/exec"
func query(name string) {
    exec.Command("nslookup", "-type=TXT", name).Output()
    exec.Command("nslookup", "-type=SRV", name).Output()
}
