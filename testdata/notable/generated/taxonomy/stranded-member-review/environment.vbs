Set shell = CreateObject("WScript.Shell")
Set env = shell.Environment("Process")
env.Item("EXAMPLE") = "value"
