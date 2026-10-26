"""dumpsys package com.example.app
FLAG_DEBUGGABLE
"""
# "FLAG_DEBUGGABLE" in result
def check(result):
    hint = '"FLAG_DEBUGGABLE" in result'
    command = "dumpsys packages com.example.app"
    return "FLAG_DEBUGGABLE_DISABLED" in result
