# An API name in prose does not establish a call.
documentation = "ctypes.windll.kernel32.CreateMutexW(None, False, 'maintenance')"

# A local declaration with the API spelling is not a Windows API invocation.
def CreateMutexW(*args):
    return 0

CreateMutexW = None
