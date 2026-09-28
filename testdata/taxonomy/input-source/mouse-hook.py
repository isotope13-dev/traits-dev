import pyHook

def on_mouse(event):
    print(event.Position)
    return True

manager = pyHook.HookManager()
manager.MouseAll = on_mouse
manager.HookMouse()
