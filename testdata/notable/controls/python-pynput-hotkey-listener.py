from pynput.keyboard import Key, Listener


def on_press(key):
    if key == Key.esc:
        return False


def run_hotkey_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()
