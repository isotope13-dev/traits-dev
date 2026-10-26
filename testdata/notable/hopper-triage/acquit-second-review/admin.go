package main
import ("os/exec"; "syscall")
func admin(target string) {
 exec.Command("TASKKILL.exe", "/F", "/IM", target).Run()
 exec.Command("net.exe", "stop", "ExampleService").Run()
 exec.Command("attrib.exe", "-R", target).Run()
 exec.Command("CMD.exe", "/C", "net", "use", "Z:").Run()
 kernel := syscall.NewLazyDLL("kernel32.dll")
 _ = kernel.NewProc("SetPriorityClass")
 exec.Command("powershell", "-Command", "Get-WmiObject -Class Win32_Volume; Get-ClusterSharedVolume").Run()
}
