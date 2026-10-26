import winreg
clsid = "{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}"
key = r"Software\Classes\TypeLib\{00020430-0000-0000-C000-000000000046}\2.0\0\win64"
print(winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, key))
example = r"script:C:\ProgramData\agent.sct"
progid = "WScript.Shell"
