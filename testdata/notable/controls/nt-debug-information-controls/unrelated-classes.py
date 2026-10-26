import ctypes
ntdll = ctypes.WinDLL("ntdll.dll")
ProcessDebugFlags = 31
ThreadHideFromDebugger = 17
reference = "NtQueryInformationProcess(-1, 31, buffer, 4, None)"
# NtSetInformationThread(-2, ThreadHideFromDebugger, None, 0)
# Neither the reference string nor these unrelated information classes is a debugger operation.
ntdll.NtQueryInformationProcess(31, 0, None, 17, None)
ntdll.NtSetInformationThread(17, 0, None, 31)
ntdll.NtQueryInformationProcess(ProcessDebugFlags, 0, None, 4, None)
ntdll.NtSetInformationThread(ThreadHideFromDebugger, 0, None, 0)
