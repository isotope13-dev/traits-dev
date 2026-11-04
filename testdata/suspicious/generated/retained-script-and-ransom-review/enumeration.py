import win32gui
win32gui.EnumWindows(lambda hwnd, data: None, None)
message="Your files have been encrypted. pay bitcoin to decrypt files."
