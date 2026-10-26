package main
import "os/exec"
func main() {
 exec.Command("schtasks", "/Create", "/SC", "ONSTART", "/TN", "Inventory", "/TR", "inventory.exe").Run()
 exec.Command("schtasks", "/Create", "/SC", "ONLOGON", "/TN", "InventoryUser", "/TR", "inventory.exe").Run()
}
