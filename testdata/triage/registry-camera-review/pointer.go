package platform
import "unsafe"
func f(mode *uint32) { api(uintptr(unsafe.Pointer(mode))) }
