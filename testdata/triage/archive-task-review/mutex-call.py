"""Inert ordinary single-instance application control; do not execute."""
import ctypes

instance = ctypes.windll.kernel32.CreateMutexW(None, False, "MaintenanceInstance")
if ctypes.windll.kernel32.GetLastError() == 183:
    raise SystemExit(0)
