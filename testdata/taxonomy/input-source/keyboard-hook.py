import pyHook

def on_key(event):
    print(event.Key)
    return True

manager = pyHook.HookManager()
manager.KeyDown = on_key
manager.HookKeyboard()
