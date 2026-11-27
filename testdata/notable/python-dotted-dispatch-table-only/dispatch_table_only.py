# Near miss: same verb vocabulary in a local dispatch table with no
# WebSocket channel, public endpoint, blackout or process verbs.
H = {
    "file.upload": handle_edit,
    "file.download": handle_cat,
    "terminal.exec": handle_exec,
    "screen.shot": handle_shot,
}
