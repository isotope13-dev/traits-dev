package ntprobe

// Benign control: a smoke test that the ntdll lazy loader resolves. Names a
// native memory API but carries no payload and queues no APC, so it must
// never reach a hostile verdict.
import (
	"testing"

	"golang.org/x/sys/windows"
)

func TestResolveAllocateStub(t *testing.T) {
	mod := windows.NewLazySystemDLL("ntdll.dll")
	proc := mod.NewProc("NtAllocateVirtualMemory")
	if proc == nil {
		t.Fatal("unresolved NtAllocateVirtualMemory")
	}
}
