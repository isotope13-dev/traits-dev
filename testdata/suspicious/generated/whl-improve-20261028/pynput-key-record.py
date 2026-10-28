from pynput import keyboard
events = []
def on_press(key):
    events.append({"key": key.char})
def record():
    return keyboard.Listener(on_press=on_press)
