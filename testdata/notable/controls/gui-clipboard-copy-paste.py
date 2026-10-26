# Benign GUI clipboard consumer: explicit user-driven copy/paste of a hex
# selection (Ctrl+Insert copies, Shift+Insert pastes), as in androguard's Qt
# hex editor. A bare pyperclip.paste() call is a neutral capability, not a
# stealer signal: nothing here monitors, polls, or exfiltrates.
import re

import pyperclip
from PyQt5 import QtCore


class HexPane:
    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                if event.key() == QtCore.Qt.Key_Insert:
                    hx = self.selected_hex()
                    pyperclip.copy(hx)

            if event.modifiers() & QtCore.Qt.ShiftModifier:
                if event.key() == QtCore.Qt.Key_Insert:
                    hx = pyperclip.paste()
                    raw = ''.join(
                        chr(int(pair, 16))
                        for pair in re.findall(r'.{1,2}', hx, re.DOTALL)
                    )
                    self.write(0, raw)
        return False
