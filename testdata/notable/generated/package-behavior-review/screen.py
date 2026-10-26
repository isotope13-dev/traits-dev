import mss
class Capture:
    def __init__(self):
        self.sct = mss.mss()
    def capture(self, monitor):
        return self.sct.grab(monitor)
