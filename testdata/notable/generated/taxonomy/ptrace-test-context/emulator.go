package kernel

// ptraceAttach implements ptrace(PTRACE_ATTACH, target) if seize is false, and
// ptrace(PTRACE_SEIZE, target, 0, opts) if seize is true. t is the caller.
func ptraceAttach(seize bool) {}

// PtraceGetRegSet implements ptrace(PTRACE_GETREGSET) by writing the
// register set given by the tracee into dst.
func PtraceGetRegSet() {}
