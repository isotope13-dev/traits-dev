// Source-only service-install coverage control. Do not execute.
package main
import ("os"; "syscall"; "unsafe")
const SERVICE_AUTO_START = 2
func main() {
 adv := syscall.NewLazyDLL("advapi32.dll")
 open := adv.NewProc("OpenSCManagerW")
 create := adv.NewProc("CreateServiceW")
 start := adv.NewProc("StartServiceW")
 scm, _, _ := open.Call(0, 0, 0xf003f)
 name, _ := syscall.UTF16PtrFromString("svchost32")
 image, _ := syscall.UTF16PtrFromString(`C:\Users\Public\svchost32.exe`)
 // A staged executable followed by an auto-start service installation.
 os.WriteFile(`C:\Users\Public\svchost32.exe`, []byte("MZ"), 0755)
 svc, _, _ := create.Call(scm, uintptr(unsafe.Pointer(name)), uintptr(unsafe.Pointer(name)), 0xf01ff, 0x10, SERVICE_AUTO_START, 1, uintptr(unsafe.Pointer(image)), 0, 0, 0, 0, 0)
 start.Call(svc, 0, 0)
}
