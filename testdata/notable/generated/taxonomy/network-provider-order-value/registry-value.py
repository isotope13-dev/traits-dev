import winreg


def configure(key):
    winreg.SetValueEx(key, "ProviderOrder", 0, winreg.REG_SZ, "NPPSpy")
