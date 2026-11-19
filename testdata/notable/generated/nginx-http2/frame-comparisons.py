def dispatch(frame_type):
    if frame_type == 1:
        return "HEADERS"
    elif frame_type == 3:
        return "RST_STREAM"
    elif frame_type == 4:
        return "SETTINGS"
