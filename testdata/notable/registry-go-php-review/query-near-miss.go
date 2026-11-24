package queries
import "os/exec"
func query(name string) {
    // exec.Command("nslookup", "-type=TXT", name)
    exec.Command("printf", "nslookup", "-type=TXT", "-type=SRV").Output()
    exec.Command("nslookup", "-type=A", name).Output()
}
