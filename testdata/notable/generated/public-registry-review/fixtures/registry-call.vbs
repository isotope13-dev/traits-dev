Sub ConfigureOwner()
 status = RegSetValueExA(key, "RegisteredOwner", 0, 1, "Example", 8)
End Sub
