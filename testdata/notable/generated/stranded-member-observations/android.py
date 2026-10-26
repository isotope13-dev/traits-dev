def inspect_app(adb, package):
    details = adb(f"dumpsys package {package}")
    return "FLAG_DEBUGGABLE" in details
