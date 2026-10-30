import keyboard
# A shortcut listener and a chat bot do not establish keystroke exfiltration.
def shortcut(event):
    print("shortcut")
keyboard.on_press(shortcut)
def create_text_channel():
    return None
